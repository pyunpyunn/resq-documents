"""Reconcile legacy use-case notes with the UI, backend policy and product boundary."""

MOBILE='resqperation-system/frontend-mobile/'
POLICY='resqperation-system/backend-laravel/app/Services/Web/WebAccessPolicy.php'


def apply_scope_rules(c):
    functions=c['functions'];modules={m['key']:m for m in c['modules']}
    # Arrival verification belongs to EvaTrack. SMS safety submission is not a
    # mobile screen; notification delivery must not imply an SMS alert channel.
    excluded={'UC13B','UC38'}
    for key in excluded:functions.pop(key,None)
    for m in c['modules']:m['cases']=[key for key in m['cases'] if key not in excluded]
    for role in c['roles']:
        role['cases']=[key for key in role['cases'] if key not in excluded]
        if role['system'] in ('household','rescuer'):role['cases'].append('UC40')
        if role['system']=='rescuer':role['cases'].append('UC41')

    modules['01_access']['providers']=['OneSignal','SMS Recovery Gateway']
    modules['03_household_setup'].update(title='First-Login Household Setup',tables=['households','household_members','addresses','geotagged_locations','device_tokens'],controllers=['HouseholdMobileController'],providers=['SafeTrack','OpenStreetMap'])
    modules['04_safety'].update(title='Household Disaster Response',providers=[])
    modules['05_alerts']['providers']=['OneSignal']
    modules['08_assessment']['tables']=[t for t in modules['08_assessment']['tables'] if t!='evacuation_records']
    modules['08_assessment']['controllers']=['RescuerMobileController']
    modules['09_navigation']['title']='Evacuation and Mission Maps'
    modules['09_navigation']['tables']+=['evacuation_centers']

    def move(key,destination):
        for m in c['modules']:
            if key in m['cases']:m['cases'].remove(key)
        modules[destination]['cases'].append(key)
        functions[key]['module']=destination

    move('UC12','09_navigation')
    move('UC13A','01_access')
    move('UC14','09_navigation')
    functions['UC40']={'id':'UC-40','key':'UC40','title':'Allow Device Location Access','description':'Choose whether the app may access device location for household geotagging or assigned rescue navigation. Manual household map pinning remains available when GPS permission is declined.','module':'01_access','source':MOBILE+'utils/mobilePermissions.ts','subcases':[]}
    functions['UC41']={'id':'UC-41','key':'UC41','title':'Update Assigned Rescue Progress','description':'Use the assigned mission controls to accept, mark en route, mark arrival and record household completion subject to the mission workflow; this is not HQ-wide dispatch approval.','module':'07_dispatch','source':MOBILE+'components/rescuer/RescuerDashboardScreen.tsx','subcases':[]}
    modules['01_access']['cases'].append('UC40');modules['07_dispatch']['cases'].append('UC41')
    # Dispatch is a mission workspace, not just an assignment-list screen.
    modules['07_dispatch']['cases']+=['UC16','UC19']

    titles={
      'UC08':'Complete First-Login Household Setup',
      'UC09':'Read Disaster Alerts and Instructions',
      'UC10':'Report Household / Member Safety',
      'UC11':'Assist a Trusted Household',
      'UC12':'View Evacuation Centers and Routes',
      'UC13A':'Display Household QR for EvaTrack',
      'UC14':'View Previously Saved Household Data',
      'UC15':'Review Assigned Rescue Mission',
      'UC16':'Follow Assigned Rescue Route',
      'UC18':'Record Rescue Member Assessment',
      'UC19':'Submit Assigned-Household Field Report',
      'UC23A':'Publish Disaster Alerts Through OneSignal',
      'UC37':'Allow App Notifications',
    }
    for key,title in titles.items():functions[key]['title']=title
    functions['UC08'].update(source=MOBILE+'hooks/useHouseholdSetup.ts',description='First-login onboarding: select the eligible phone owner when required, confirm the household map location and address/apartment details, and optionally add a household photo. This does not publish alerts, report disaster safety or verify evacuation arrival.',phase='First-Login Household Setup',subcases=[('Set / Confirm Household Geotag','include'),('Confirm Address / Apartment Details','include'),('Select Phone Owner If Required','extend'),('Add Household Photo','extend')])
    functions['UC37'].update(source=MOBILE+'components/NotificationPermissionNotice.tsx',description='Use the Enable notifications prompt or device notification settings. OneSignal registration is automatic background behavior, not a separate user-facing subscription screen.',subcases=[],phase='Account Access and Permissions',system_titles={'household':'Allow Disaster Notifications','rescuer':'Allow Assignment Notifications'})
    functions['UC40'].update(phase='Account Access and Permissions',system_titles={'household':'Allow Location for Home Geotag','rescuer':'Allow Location for Rescue Routes'})
    functions['UC13A'].update(description='Display the household identity QR; EvaTrack is responsible for evacuation-arrival verification.',phase='Household Profile and Identity',subcases=[])
    functions['UC02']['system_subcases']={
      'household':[('Edit Personal Contact Details','extend'),('Update Saved Home Geotag','extend'),('Change Own Password','extend')],
      'rescuer':[('Edit Own Rescuer Profile','extend'),('Change Own Password','extend')],
      'web':[('Edit Own Staff Profile','extend'),('Change Own Password','extend')],
    }
    functions['UC09'].update(phase='Disaster Alerts and Safety',subcases=[('Read Active Disaster Instructions','include'),('Review Previous Disaster Alerts','extend')])
    functions['UC10'].update(phase='Disaster Alerts and Safety',subcases=[('Select Current Disaster Status','include'),('Add Member Safety Details','extend'),('Review Submitted Safety History','extend')])
    functions['UC11'].update(phase='Disaster Alerts and Safety',subcases=[('Verify Trusted Household PIN','include'),('Submit Authorized Member Status','extend')])
    functions['UC12'].update(phase='Evacuation Maps and Saved Data',subcases=[('View Evacuation Center Map','include'),('Follow Available Evacuation Route','extend')])
    functions['UC14']['phase']='Evacuation Maps and Saved Data'
    functions['UC15'].update(phase='Assigned Rescue Missions',source=MOBILE+'components/rescuer/RescuerDashboardScreen.tsx',subcases=[('View Household and Member Details','include')])
    functions['UC16'].update(phase='Assigned Rescue Missions',source=MOBILE+'components/rescuer/RescueMapScreen.native.tsx',subcases=[('Open Assigned Mission Route Map','include'),('Share Location With HQ','extend')])
    functions['UC41'].update(phase='Assigned Rescue Missions',subcases=[('Accept Assigned Rescue Mission','extend'),('Mark Mission En Route','extend'),('Mark Arrival at Assigned Household','extend'),('Record Household Mission Completion','extend')])
    functions['UC18'].update(phase='Rescue Field Assessments',description='Assess members of an assigned rescue household. Rescue check-ins are separate from EvaTrack evacuation-center arrival verification.',subcases=[('Select Assigned Household Members','include'),('Record Member Safety Conditions','include')])
    functions['UC19'].update(title='Submit Assigned Field Report If Needed',phase='Assigned Rescue Missions',source=MOBILE+'components/rescuer/FieldReportScreen.tsx',description='Submit a field report for the assigned household when applicable: record member conditions and property damage, review injury/death totals derived from member statuses, and optionally add notes.',subcases=[('Record Member Safety Conditions','include'),('Record Household Property Damage','include'),('Add Field Notes If Applicable','extend')])
    # Publish / approve are distinct from receiving alerts or merely seeing a module.
    restricted={
      'UC04':{'operationsadmin'},'UC05':{'operationsadmin'},'UC06':{'operationsadmin'},
      'UC23A':{'chair','operationsadmin'},'UC26B':{'chair','operationsadmin','response'},
      'UC26C':{'chair','operationsadmin'},'UC32B':{'chair','operationsadmin'},'UC33':{'chair','operationsadmin'},
    }
    for key,allowed in restricted.items():
        for role in c['roles']:
            if role['actor'] not in allowed and key in role['cases']:role['cases'].remove(key)
        functions[key]['source_policy']=POLICY
    human_actors={r['actor'] for r in c['roles']}
    for f in functions.values():
        f['external_actors']=[c['actors'][a] for a in f.get('actors',[]) if a not in human_actors and a in c['actors']]
        f['module_title']=modules[f['module']]['title']
        f['roles']=[r['title'] for r in c['roles'] if f['key'] in r['cases']]
        f['actors']=[r['actor'] for r in c['roles'] if f['key'] in r['cases']]
        f['systems']=sorted({r['system'] for r in c['roles'] if f['key'] in r['cases']}) or ['web']
        f['related_modules']=[m['key'] for m in c['modules'] if f['key'] in m['cases']]
        if 'phase' not in f:
            f['phase']='Account Access and Permissions' if f['module']=='01_access' else f['module_title']
    for role in c['roles']:role['cases']=sorted(set(k for k in role['cases'] if k in functions))
    for m in c['modules']:m['cases']=list(dict.fromkeys(k for k in m['cases'] if k in functions))
    c['scope_corrections']={
      'excluded_use_cases':{'UC13B':'Evacuation-arrival verification belongs to EvaTrack.','UC38':'No SMS disaster-alert or user-facing SMS safety-submission feature is depicted.'},
      'disaster_alert_provider':'OneSignal',
      'sms_scope':'Configured account recovery only; never disaster-alert delivery.',
      'permission_ui':MOBILE+'components/NotificationPermissionNotice.tsx',
      'location_consent_ui':MOBILE+'utils/mobilePermissions.ts',
      'first_login_setup':MOBILE+'hooks/useHouseholdSetup.ts',
      'rescuer_mission_ui':MOBILE+'components/rescuer/RescuerDashboardScreen.tsx',
      'role_policy':POLICY,
    }
    return c
