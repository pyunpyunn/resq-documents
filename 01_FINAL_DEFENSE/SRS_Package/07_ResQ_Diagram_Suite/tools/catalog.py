"""Build diagram content from the repository's current diagram and API evidence."""
from pathlib import Path
import csv
import json
import re
from scope_rules import apply_scope_rules

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[3]
PACKAGE = OUT.parent
UCROOT = PACKAGE / '02_Use_Cases_and_Narratives'
ERROOT = PACKAGE / '04_ERD'
BACKEND = ROOT / 'resqperation-system/backend-laravel'

MODULES = [
    ('01_access', 'Account Access', ['users','roles','personal_access_tokens','password_reset_requests','password_reset_tokens','device_tokens','remembered_devices','notifications','web_push_subscriptions','web_push_deliveries'], ['AuthController','ProfileController','MobileDeviceController','NotificationController'], ['SMS Gateway','OneSignal']),
    ('02_administration', 'Administration', ['users','roles','responders','rescue_teams','landing_inquiries','barangays','audit_logs'], ['RescuerAccountController','PersonnelRoleController','InquiryController','ProfileController'], []),
    ('03_household_setup', 'Household Setup', ['households','household_members','addresses','geotagged_locations','evacuation_centers','evacuation_records'], ['HouseholdMobileController','EvacuationCheckInController'], ['SafeTrack','OSRM']),
    ('04_safety', 'Household Safety', ['household_disasters','household_status_logs','member_status_logs','member_disaster_statuses','household_statuses','member_statuses','trusted_households','household_trusted_pins'], ['HouseholdStatusController','HouseholdMobileController','SmsInboundController'], ['SMS Gateway']),
    ('05_alerts', 'Disaster Alerts', ['disaster_events','disaster_event_types','disaster_broadcasts','disaster_types','severity_levels','status_reminders','notifications','device_tokens','household_mobile_notifications','web_push_deliveries'], ['DisasterBroadcastController'], ['OneSignal','SMS Gateway']),
    ('06_monitoring', 'Operational Monitoring', ['disaster_events','household_disasters','household_status_logs','households','geotagged_locations','mapping_hazard_layers','weather_logs','rescue_criteria_snapshots','rescue_criteria_line_snapshots','rescue_priority_settings'], ['DashboardController','MappingController','WeatherController','HazardLayerController','HouseholdDirectoryController','GlobalSearchController'], ['Open-Meteo','PAGASA','OpenStreetMap','Esri']),
    ('07_dispatch', 'Rescue Dispatch', ['responder_assignments','rescue_teams','responders','dispatch_statuses','household_disasters','rescue_priority_settings','rescue_criteria_snapshots','rescue_criteria_contact_baselines','rescue_criteria_line_snapshots'], ['RescueDispatchController','RescuerMobileController'], ['OneSignal']),
    ('08_assessment', 'Field Assessment', ['responder_check_ins','responder_field_reports','responder_field_report_details','responder_field_report_members','hq_field_reports','field_report_categories','property_damage_levels','evacuation_records','member_disaster_statuses'], ['RescuerMobileController','EvacuationCheckInController'], []),
    ('09_navigation', 'Mission Navigation', ['cached_routes','offline_packs','dispatch_trips','trip_points','route_coordinates','device_tracking_logs','responder_location_logs','responder_routes','sync_events','map_tile_metadata'], ['MobileNavigationController'], ['Valhalla','OSRM','OpenStreetMap']),
    ('10_radio', 'Field Communication', ['responder_communication_logs','responder_assignments','responders','users'], ['RescuerMobileController','RescueDispatchController'], []),
    ('11_requests', 'Resource Requests', ['resource_requests','request_validations','resource_request_status','urgency_levels'], ['ResourceRequestController'], ['EvaTrack','TrackingAid']),
    ('12_reports', 'Reports and Archives', ['situation_reports','situation_report_submissions','external_report_requests','incident_archives','hq_field_reports','responder_field_reports','resource_requests','audit_logs'], ['SituationReportController','ArchiveController','ExternalReportController','ReportExchangeController','EvaTrackReportController'], ['SafeTrack','EvaTrack','TrackingAid']),
]
ROLE_INFO = [
    ('01_public','Public Visitor','public','web'),
    ('02_household_resident','Household Resident','householdresident','household'),
    ('03_tl','Rescuer Team Leader','tl','rescuer'),
    ('04_tm','Rescuer Team Member','tm','rescuer'),
    ('05_chair','Chairperson','chair','web'),
    ('06_operations_admin','Operations / Admin','operationsadmin','web'),
    ('07_mitigation_prevention','Mitigation / Prevention','mitigationprevention','web'),
    ('08_preparedness','Preparedness','preparedness','web'),
    ('09_response','Response Personnel','response','web'),
    ('10_recovery_rehabilitation','Recovery / Rehabilitation','recoveryrehabilitation','web'),
]
SHORT = {
 'UC01':'Sign In / Out','UC02':'Update Own Profile','UC03':'Recover Account Access',
 'UC04':'Manage Rescuer Teams','UC05':'Manage HQ Access','UC06':'Maintain Barangay Profile',
 'UC07A':'Submit Public Inquiry','UC07B':'Review Public Inquiries','UC08':'Complete Household Setup',
 'UC09':'Review Disaster Alerts','UC10':'Report Household Safety','UC11':'Assist Trusted Households',
 'UC12':'View Evacuation Routes','UC13A':'Display Verification QR','UC13B':'Verify Evacuation Arrival',
 'UC14':'Read Saved Household','UC15':'View Assigned Incidents','UC16':'Navigate Assigned Mission',
 'UC17':'Synchronize Saved Trips','UC18':'Assess Household Members','UC19':'Submit Field Findings',
 'UC20A':'Transmit PTT Clips','UC20B':'Monitor Rescue Communications','UC21A':'Submit Logistics Request',
 'UC21B':'Track Own Requests','UC22A':'Monitor Operations Dashboard','UC22B':'Review Operational Maps',
 'UC23A':'Publish Disaster Alerts','UC23B':'Manage Active Event','UC24':'Review Hazard Overlays',
 'UC25A':'Review Safety Reports','UC25B':'Confirm Household Status','UC26A':'Inspect Rescue Priorities',
 'UC26B':'Dispatch Rescue Team','UC26C':'Approve Dispatch Completion','UC27':'Monitor Field Progress',
 'UC28':'Prepare Situation Reports','UC29':'Export Escalation Findings','UC30':'Manage Archive Evidence',
 'UC31':'Submit Partner Request','UC32A':'Review Resource Requests','UC32B':'Validate Resource Requests',
 'UC33':'Forward Validated Requests','UC34A':'Request Operational Report','UC34B':'Authorize Report Release',
 'UC35':'Review Partner Reports','UC36':'Export Selected Findings','UC37':'Register Push Subscription',
 'UC38':'Submit SMS Safety','UC39':'Review Web Notifications',
}
SUBCASES = {
 'UC01':[('Verify Credentials','include'),('Validate Account Scope','include')],
 'UC10':[('Validate Event Scope','include'),('Save Status Evidence','include')],
 'UC12':[('Calculate Available Route','extend')],
 'UC19':[('Validate Field Evidence','include')],
 'UC20A':[('Validate Team Scope','include')],
 'UC26B':[('Validate Dispatch Targets','include'),('Save Assignment','include')],
 'UC28':[('Compile Recorded Findings','include')],
 'UC32B':[('Check Approval Rights','include')],
 'UC33':[('Queue Partner Handoff','include')],
 'UC34B':[('Generate Signed File','extend')],
}


def read_cases(path):
    text=path.read_text(encoding='utf-8')
    cases=dict(re.findall(r'case(UC\w+)\(\["([^"]+)"\]\)',text))
    actors=dict(re.findall(r'actor(\w+)\["Actor: ([^"]+)"\]',text))
    links=re.findall(r'actor(\w+)\s+---\s+case(UC\w+)',text)
    return cases,actors,links


def parse_schema():
    text=(ERROOT/'01_UNIFIED/01_full_physical_erd.mmd').read_text(encoding='utf-8')
    tables={}; aliases={}
    for match in re.finditer(r'^  (\w+)\["([^"]+)"\] \{(.*?)\n  \}',text,re.M|re.S):
        alias,label,body=match.groups();name=label.split(' (')[0]
        if '(VIEW)' in label or name.startswith('_archive_'):continue
        rows=[]
        for line in body.splitlines():
            m=re.match(r'\s*(\w+)\s+(\w+)\s*(.*)',line)
            if m:rows.append({'type':m[1],'name':m[2],'keys':[k.strip() for k in m[3].split(',') if k.strip()]})
        tables[name]={'name':name,'alias':alias,'scope':label.split(' (')[-1].rstrip(')'), 'fields':rows}
        aliases[alias]=name
    rels=[]
    for a,card,b,col in re.findall(r'^  (\w+)\s+([|o{}.:\-]+)\s+(\w+)\s+:\s+"([^"]+)"',text,re.M):
        if a not in aliases or b not in aliases:continue
        parent,child=aliases[a],aliases[b]
        parent_pk=next((f['name'] for f in tables[parent]['fields'] if 'PK' in f['keys']),None)
        rel={'parent':parent,'child':child,'column':col,'parent_column':parent_pk,'cardinality':card,'physical':True}
        rels.append(rel)
        for f in tables[child]['fields']:
            if f['name']==col:f['references']=parent
    assert all(any('PK' in f['keys'] for f in t['fields']) for t in tables.values())
    return tables,rels


def build_catalog():
    roles=[];all_links={};all_actors={}
    for key,label,actor,system in ROLE_INFO:
        path=UCROOT/'03_USER_ROLES'/f'{key}.mmd'
        cases,actors,links=read_cases(path)
        roles.append({'key':key,'title':label,'actor':actor,'system':system,'cases':sorted({c for a,c in links if a==actor}),'source':str(path.relative_to(ROOT))})
    functions={};modules=[]
    for key,title,tables,controllers,providers in MODULES:
        path=UCROOT/'02_MODULES'/f'{key}_use_cases.mmd'
        cases,actors,links=read_cases(path);all_actors.update(actors)
        m={'key':key,'title':title,'tables':tables,'controllers':controllers,'providers':providers,'cases':list(cases),'source':str(path.relative_to(ROOT))}
        modules.append(m)
        for case,long_title in cases.items():
            linked=[a for a,c in links if c==case]
            systems=sorted({r['system'] for r in roles if r['actor'] in linked})
            functions[case]={'id':case.replace('UC','UC-',1),'key':case,'title':SHORT[case],'description':long_title.split(': ',1)[-1],'module':key,'module_title':title,'actors':linked,'systems':systems or ['web'],'roles':[r['title'] for r in roles if case in r['cases']],'source':str(path.relative_to(ROOT)),'subcases':SUBCASES.get(case,[])}
    tables,rels=parse_schema()
    for m in modules:assert all(t in tables for t in m['tables']),m['key']
    routes=json.loads((OUT/'assets/api-routes.json').read_text(encoding='utf-8-sig'))
    return apply_scope_rules({'roles':roles,'modules':modules,'functions':functions,'actors':all_actors,'tables':tables,'relationships':rels,'routes':routes})


def export_catalog(c):
    (OUT/'assets/catalog.json').write_text(json.dumps(c,indent=2,ensure_ascii=False),encoding='utf-8')
    (OUT/'assets/scope-corrections.json').write_text(json.dumps(c['scope_corrections'],indent=2),encoding='utf-8')
    with (OUT/'FUNCTION_LIST.csv').open('w',newline='',encoding='utf-8-sig') as file:
        w=csv.writer(file);w.writerow(['Function ID','Function','Primary Module / Feature','Related Modules','User Roles','Client Systems','Related Backend Controllers','Source Evidence'])
        for f in c['functions'].values():
            m=next(m for m in c['modules'] if m['key']==f['module'])
            w.writerow([f['id'],f['title'],f['module_title'],'; '.join(f['related_modules']),'; '.join(f['roles']) or 'Partner / configured provider','; '.join(f['systems']),'; '.join(m['controllers']),f['source']])
    with (OUT/'API_FUNCTION_LIST.csv').open('w',newline='',encoding='utf-8-sig') as file:
        w=csv.writer(file);w.writerow(['Method','Endpoint','Controller / Handler','Middleware','Route Name'])
        for r in c['routes']:w.writerow([r['method'],'/'+r['uri'],r['action'],'; '.join(r['middleware']),r.get('name') or ''])
    lines=['# RESQPERATION Function List','',f"{len(c['functions'])} functional use cases across 12 modules; {len(c['routes'])} live Laravel route declarations inventoried.",'','This is source-backed logical documentation, not deployment or partner acceptance evidence. Role access is subject to backend permission configuration.','']
    for m in c['modules']:
        lines.extend([f"## {m['title']}",'','| ID | Function | User roles |','| --- | --- | --- |'])
        for key in m['cases']:
            f=c['functions'][key];lines.append(f"| {f['id']} | {f['title']} | {', '.join(f['roles']) or 'Partner / configured provider'} |")
        lines.extend(['',f"Source: `{m['source']}`",f"Related tables: {', '.join('`'+t+'`' for t in m['tables'])}.",''])
    lines.extend(['## Scope and interpretation','',
      '- Legacy use-case sources are reconciled with current mobile UI, WebAccessPolicy and the requested product boundaries. Corrections and evidence are recorded in `assets/scope-corrections.json`. Endpoints/middleware come from the Laravel route inventory.',
      '- The ERD uses the package\'s physical-schema snapshot. Views and legacy recovery tables are excluded from table diagrams; they remain in the original reference sources. Shared tables are not claimed as RESQPERATION-owned.',
      '- Full and role flow/swimlane diagrams illustrate scoped operating paths; module views contain the detailed decision and error branches.',
      '- Provider delivery, deployed navigation packs, signed-link expiry, partner acceptance, and physical-device behavior remain conditional on their running configuration.',
      '- EvaTrack owns evacuation-arrival verification. RESQPERATION may display a household QR; legacy verification endpoints in the API inventory do not make verification a RESQPERATION user responsibility.',
      '- Disaster and assignment notifications use OneSignal. The SMS recovery integration, where depicted, is limited to configured account recovery and never represents SMS disaster-alert delivery.',
      '- First-login household setup is separate from disaster operations. It covers phone-owner selection when required, household geotag/address confirmation and optional photo capture. Evacuation maps, safety reports and current-disaster instructions are not onboarding tasks.',
      '- Notification and location permissions are real user consent actions. Push-subscription registration is automatic background behavior, not a separate user-facing screen.',
      '- Rescuers may review assigned households, open the assigned route, update permitted mission progress and submit field reports when applicable. Creating dispatches, publishing alerts and approving closure remain separate authorized HQ actions.',
      '- DFD entity copies denote the same logical actor; local copies avoid long connector bundles across process rows.',
      '- A physical FK is drawn only when present in the schema source. Polymorphic / JSON / partner references are not invented as foreign keys.',
      '- Full ERDs retain physical table and column names. Compact views retain primary and foreign keys; the detailed full view retains all fields.',
      '- Dense non-planar graphs can require 90-degree crossings. Routing checks prevent connectors from passing through unrelated cards; compact, module and role views reduce congestion.',
    ])
    (OUT/'FUNCTION_LIST.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


if __name__=='__main__':
    c=build_catalog();export_catalog(c)
    print(f"Catalog: {len(c['functions'])} functions; {len(c['tables'])} physical tables; {len(c['relationships'])} FKs; {len(c['routes'])} API routes.")
