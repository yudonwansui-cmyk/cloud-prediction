from pathlib import Path
import csv, hashlib, json, sys
root=Path(__file__).resolve().parents[1]
def rows(name):
    with (root/name).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
d=rows('feature_dictionary_p24_106.csv'); g=rows('feature_group_mapping_p24.csv'); e=rows('excluded_features.csv')
s=json.loads((root/'schema_and_version.json').read_text(encoding='utf-8'))
names=[r['feature_name'] for r in d]
checks={'106_unique':len(names)==106 and len(set(names))==106,'98_numeric_8_categorical':sum(r['data_type']=='numeric' for r in d)==98 and sum(r['data_type']=='categorical' for r in d)==8,'seven_groups':set(r['physical_group'] for r in d)=={'G1','G2','G3','G4','G5','G6','G7'},'group_mapping_exact':set(names)==set(r['feature_name'] for r in g),'excluded_only_sequence_time':len(e)==1 and e[0]['feature_name']=='normalized_sequence_time','dictionary_sha256':hashlib.sha256((root/'feature_dictionary_p24_106.csv').read_bytes()).hexdigest()==s['feature_dictionary_sha256'],'relative_paths':all(not r['source_file'].startswith(('C:','/')) for r in d)}
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks}
(root/'validation/validation_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2));sys.exit(0 if all(checks.values()) else 1)
