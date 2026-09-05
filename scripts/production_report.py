"""Record production QA; only documented alpha FontBakery exceptions are allowed."""
from pathlib import Path
import json, subprocess, sys
import ots

root=Path(__file__).resolve().parents[1]
reports=root/'docs'
ots_results=[]
for path in sorted((root/'dist').glob('*.ttf')):
    result=ots.sanitize(str(path), capture_output=True)
    ots_results.append({'file':path.name,'returncode':result.returncode,
        'output':(result.stdout+result.stderr).decode(errors='replace')})
(reports/'ots-report.json').write_text(json.dumps(ots_results,indent=2))
if any(r['returncode'] for r in ots_results):
    raise SystemExit('OpenType sanitizer failed; see docs/ots-report.json')
for profile,glob,out in [('universal','Damonic-*.ttf','fontbakery-base.json'),
                         ('opentype','DamonicNerdFontMono-*.ttf','fontbakery-nerd-opentype.json')]:
    result=subprocess.run([sys.executable,'-m','fontbakery','check-'+profile,
        '--skip-network','-q','--json',str(reports/out),
        *[str(p.relative_to(root)) for p in sorted((root/'dist').glob(glob))]],cwd=root)
    if result.returncode not in (0,1):
        raise SystemExit('FontBakery did not finish normally')
    data=json.loads((reports/out).read_text())
    unexpected=[c['module'] for section in data['sections'] for c in section['checks']
        if c['result'] in ('ERROR','FATAL') or
        (c['result']=='FAIL' and c['module'] not in ('no_mac_entries','smart_dropout'))]
    if unexpected:
        raise SystemExit('Unexpected FontBakery failures: '+', '.join(unexpected))
print('Production reports generated; known alpha exceptions remain documented.')
