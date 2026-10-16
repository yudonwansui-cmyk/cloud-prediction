"""Check public package consistency; no upstream numerical audit."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import re

TIER_COUNTS = {'A0': 8, 'A1': 4, 'A2': 8, 'A3': 81, 'A4': 5}
CUMULATIVE_COUNTS = {'T0': 8, 'T1': 12, 'T2': 20, 'T3': 101, 'T4': 106}
VALUE_NAMES = [
    'shading_ratio', 'shadow_ratio_dt', 'newly_shaded_ratio', 'newly_recovered_ratio',
    'P_rec', 'P_loss', 'afd_violation_ratio', 'q_max', 'panel_q_std_max',
    'frame_panel_q_mean_dt_abs_max', 'frame_panel_q_mean_dt_positive_max',
    'frame_panel_q_mean_dt_negative_magnitude_max',
]
OPERATORS = {'mean', 'std', 'min', 'max', 'range', 'delta', 'trend', 'recent4_mean', 'recent8_mean'}
ENDPOINT_MODELS = {'E1': 'M6', 'E2': 'M5', 'E3': 'M1-v2'}


def read_rows(root, name):
    with (root / name).open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def validate(root):
    dictionary = read_rows(root, 'feature_dictionary_106.csv')
    groups = read_rows(root, 'feature_group_mapping.csv')
    excluded = read_rows(root, 'excluded_features.csv')
    channels = read_rows(root, 'sequence_channel_dictionary_25.csv')
    selections = read_rows(root, 'selected_features_by_model_fold.csv')
    schema = json.loads((root / 'schema_and_version.json').read_text(encoding='utf-8'))
    by_name = {row['feature_name']: row for row in dictionary}
    names = set(by_name)
    checks = {}
    checks['106_unique'] = len(dictionary) == len(names) == 106
    checks['106_frozen_ids'] = len({r['feature_id'] for r in dictionary}) == 106 and {r['feature_id'] for r in dictionary} == {f'F{i:03d}' for i in range(1, 107)}
    checks['98_numeric_8_categorical'] = Counter(r['data_type'] for r in dictionary) == {'numeric': 98, 'categorical': 8}
    checks['seven_groups'] = {r['physical_group'] for r in dictionary} == {f'G{i}' for i in range(1, 8)}
    checks['group_mapping_exact'] = len(groups) == len({r['feature_name'] for r in groups}) == 106 and {r['feature_name'] for r in groups} == names
    checks['group_mapping_labels'] = all(r['feature_name'] in by_name and all(r[key] == by_name[r['feature_name']][key] for key in ('physical_group', 'group_description_en')) for r in groups)
    checks['feature_tier_counts'] = Counter(r['feature_tier'] for r in dictionary) == TIER_COUNTS
    checks['first_included_tier'] = all(r['feature_tier'] in TIER_COUNTS and r['first_included_tier'] == 'T' + r['feature_tier'][1:] for r in dictionary)
    checks['cumulative_tier_counts'] = all(sum(r['first_included_tier'] <= tier for r in dictionary) == count for tier, count in CUMULATIVE_COUNTS.items())
    history = defaultdict(list)
    for row in dictionary:
        if row['feature_tier'] == 'A3':
            history[row['base_quantity']].append(row)
    checks['81_history_9_bases_9_operators'] = len(history) == 9 and all(len(items) == 9 and {r['transform_operator'] for r in items} == OPERATORS for items in history.values())
    checks['history_formula_ids'] = all(r['formula_id'] == 'H20_' + r['transform_operator'].upper() for items in history.values() for r in items)
    formula_text = (root / 'feature_formulas.md').read_text(encoding='utf-8')
    checks['history_formula_references'] = all(r['formula_id'] in formula_text for items in history.values() for r in items)
    checks['missingness_fields_present'] = all(r['raw_missing_rule'].strip() and r['imputation_rule'].strip() and 'raw_missing_rule' in r['missing_handling'] and 'imputation_rule' in r['missing_handling'] for r in dictionary)
    checks['excluded_only_sequence_time'] = len(excluded) == 1 and excluded[0]['feature_name'] == 'normalized_sequence_time' and 'normalized_sequence_time' not in names
    checks['dictionary_sha256'] = hashlib.sha256((root / 'feature_dictionary_106.csv').read_bytes()).hexdigest() == schema['feature_dictionary_sha256']
    checks['schema_counts'] = schema['feature_count'] == 106 and schema['feature_tier_counts'] == TIER_COUNTS and schema['cumulative_tier_counts'] == CUMULATIVE_COUNTS
    checks['cohort_metadata'] = {key: value['cloud_count'] for key, value in schema['cohort_terminology'].items()} == {'development_cohort': 810, 'descriptive_evaluation_cohort': 203, 'full_cloud_cohort': 1013} and schema['cohort_terminology']['descriptive_evaluation_cohort']['previously_used_in_research'] is True
    checks['classification_population'] = schema['classification_population_clouds'] == 1013 and schema['classification_used_evaluation_covariates'] is True
    checks['sequence_shape'] = schema['sequence_shape'] == [11, 25] and schema['sequence_channel_index_base'] == 0
    checks['25_ordered_unique_channels'] = [r['channel_index'] for r in channels] == [str(i) for i in range(25)] and len({r['channel_name'] for r in channels}) == 25
    checks['channel_roles'] = [r['channel_role'] for r in channels] == ['value'] * 12 + ['missing_indicator'] * 12 + ['observed_time_mask']
    checks['channel_base_order'] = [r['base_feature_name'] for r in channels] == VALUE_NAMES + VALUE_NAMES + ['']
    checks['channel_names_and_units'] = [r['channel_name'] for r in channels] == VALUE_NAMES + [n + '__missing' for n in VALUE_NAMES] + ['observed_time_mask'] and [r['channel_unit'] for r in channels] == ['standardized'] * 12 + ['indicator'] * 13
    checks['channel_base_mapping'] = len(channels) == 25 and all(r['base_feature_name'] in by_name and r['physical_group'] == by_name[r['base_feature_name']]['physical_group'] and r['base_unit'] == by_name[r['base_feature_name']]['unit'] for r in channels[:24]) and all(channels[24][key] == '' for key in ('base_feature_name', 'physical_group', 'base_unit'))
    sequence_text = (root / 'sequence_input_11x25.md').read_text(encoding='utf-8')
    checks['sequence_markdown_order'] = re.findall(r'^\d+\. `([^`]+)`', sequence_text, flags=re.MULTILINE) == VALUE_NAMES
    selection_keys = [(r['endpoint'], r['model_id'], r['repeat'], r['outer_fold'], r['input_branch'], r['feature_name']) for r in selections]
    checks['selected_rows_unique'] = bool(selections) and len(selection_keys) == len(set(selection_keys))
    expected_scope = {(endpoint, model, '0', str(fold)) for endpoint, model in ENDPOINT_MODELS.items() for fold in range(5)}
    checks['selected_scope'] = {(r['endpoint'], r['model_id'], r['repeat'], r['outer_fold']) for r in selections} == expected_scope and {r['input_branch'] for r in selections} == {'static', 'sequence_value'}
    checks['selected_feature_names_and_groups'] = all(r['feature_name'] in by_name and r['physical_group'] == by_name[r['feature_name']]['physical_group'] for r in selections)
    values_by_scope = defaultdict(list)
    for row in selections:
        if row['input_branch'] == 'sequence_value':
            values_by_scope[(row['endpoint'], row['model_id'], row['repeat'], row['outer_fold'])].append(row)
    checks['selected_sequence_indices'] = set(values_by_scope) == {key for key in expected_scope if key[0] in {'E1', 'E2'}} and all(len(items) == 12 and {r['channel_index']: r['feature_name'] for r in items} == {str(i): name for i, name in enumerate(VALUE_NAMES)} for items in values_by_scope.values())
    checks['static_channel_index_empty'] = all(r['channel_index'] == '' for r in selections if r['input_branch'] == 'static')
    scope = schema['selected_input_scope']
    checks['schema_selection_scope'] = scope['repeat'] == 0 and scope['outer_folds'] == list(range(5)) and scope['endpoint_models'] == ENDPOINT_MODELS and scope['final_development_refit'] is False
    forbidden = {
        'source_tier', 'source_file', 'source_function_or_line', 'upstream_column',
        'upstream_source_file', 'upstream_source_function_or_line', 'evidence_status',
        'original_registry', 'excluded_from', 'evidence_file', 'evidence_location',
    }
    tables = [dictionary, groups, excluded, channels, selections]
    checks['implementation_provenance_absent'] = not (root / 'feature_source_trace_public.csv').exists() and all(
        not forbidden.intersection(row) and not any(key.endswith('_zh') for key in row)
        for table in tables for row in table)
    checks['english_only_content'] = all(
        re.search(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]',
                  path.read_text(encoding='utf-8-sig')) is None
        for path in [root.parent.parent / 'README.md', *root.rglob('*')]
        if path.is_file() and path.suffix in {'.md', '.csv', '.json', '.py'})
    checks['language_metadata'] = schema['documentation_language'] == 'en' and schema['implementation_provenance_included'] is False and all(
        'label_zh' not in cohort for cohort in schema['cohort_terminology'].values())
    return {'status': 'PASS' if all(checks.values()) else 'FAIL',
            'validation_scope': 'Public documentation consistency only; no upstream numerical or private-registry audit.',
            'checks': checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1], help='Package directory to validate.')
    args = parser.parse_args()
    try:
        result = validate(args.root)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        result = {'status': 'FAIL', 'checks': {'readable_valid_inputs': False}, 'error': str(error)}
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    result_path = args.root / 'validation' / 'validation_result.json'
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_bytes(output.encode('utf-8'))
    print(output, end='')
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
