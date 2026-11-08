# ResQperation — Push Notification Setup
> Disaster broadcast alerts for household and rescuer mobile accounts
> Provider: Expo Push Notification Service (free, no third-party cost)
> Last updated: May 2025

---

## Table of Contents
1. [Why Expo Push Service](#1-why-expo-push-service)
2. [How it works — the full flow](#2-how-it-works--the-full-flow)
3. [Cost and limits](#3-cost-and-limits)
4. [Setup — Mobile (React Native)](#4-setup--mobile-react-native)
5. [Setup — Back end (Laravel)](#5-setup--back-end-laravel)
6. [Sending a broadcast — the full code](#6-sending-a-broadcast--the-full-code)
7. [Broadcast rules by disaster type](#7-broadcast-rules-by-disaster-type)
8. [Testing without a real device](#8-testing-without-a-real-device)
9. [Common errors and fixes](#9-common-errors-and-fixes)

---

## 1. Why Expo Push Service

You are already using Expo for your mobile app. Expo has its own built-in push
notification service that sits on top of Firebase Cloud Messaging (FCM) for
Android and Apple Push Notification Service (APNs) for iOS.

**You do not need to set up Firebase or Apple developer accounts separately.**
Expo handles all of that for you behind the scenes.

| Option | Cost | Setup complexity | Works with Expo managed workflow |
|---|---|---|---|
| **Expo Push Service** ✅ | Free | Simple | Yes — out of the box |
| Firebase FCM directly | Free | Complex (needs Firebase project + config) | Needs extra setup |
| OneSignal | Free tier (limited) | Medium | Yes but needs SDK |
| AWS SNS | Pay per notification | Very complex | Yes but overkill |

**Use Expo Push Service. It is the correct choice for this project.**

Limits that matter for ResQperation:
- **600 notifications per second** per project — for a barangay of 1,248 households
  this sends all notifications in under 3 seconds
- **No monthly limit** on total notifications sent
- **No cost** — completely free for non-commercial use

---

## 2. How it works — the full flow

```
[HQ Dispatcher clicks "Send Broadcast" on web dashboard]
         ↓
[Laravel back end saves broadcast to resq_broadcasts table]
         ↓
[Laravel fetches all expo_push_tokens for target users
 (all users, rescuers only, or specific purok)]
         ↓
[Laravel sends POST request to https://exp.host/--/api/v2/push/send
 with all tokens and the message]
         ↓
[Expo Push Service routes to FCM (Android) or APNs (iOS)]
         ↓
[Mobile device receives notification — even if app is closed]
         ↓
[User taps notification → app opens to Alerts screen]
```

The only external service involved is Expo's server at `exp.host`.
No Firebase console. No Apple developer account. No third-party dashboard.

---

## 3. Cost and Limits

| What | Limit |
|---|---|
| Cost | **Free** |
| Notifications per second | 600 (sends 1,248 HH alerts in ~2 seconds) |
| Notifications per request | Max 100 tokens per request (batch them — code below handles this) |
| Total monthly notifications | **Unlimited** |
| API key required | Optional (free Expo account for access token if you want extra security) |

For a barangay with 1,248 households + ~20 rescuers = ~1,268 tokens.
Batched at 100 per request = 13 requests. All sent in under 5 seconds.

---

## 4. Setup — Mobile (React Native)

### Step 1 — Install the package

```bash
cd mobile
npx expo install expo-notifications expo-device
```

### Step 2 — Request permission and get the push token

Every time the mobile app starts, it must register the device and save
the Expo push token to your Laravel back end.

```javascript
// mobile/api/notifications.js

import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import api from './axios';

// Call this once when the user logs in
export async function registerPushToken() {
  // Only works on a real device, not a simulator
  if (!Device.isDevice) {
    console.log('Push notifications only work on real devices');
    return;
  }

  // Ask the user for permission
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  if (finalStatus !== 'granted') {
    console.log('Permission not granted for push notifications');
    return;
  }

  // Get this device's unique Expo push token
  const tokenData = await Notifications.getExpoPushTokenAsync({
    projectId: 'your-expo-project-id', // get this from app.json > expo.extra.eas.projectId
  });

  const token = REDACTED;

  // Save token to your Laravel back end
  await api.post('/push-tokens', { token });

  return token;
}
```

### Step 3 — Call registerPushToken after login

```javascript
// mobile/app/(household)/home.jsx  OR  mobile/app/(rescuer)/home.jsx
// Add this inside the useEffect that runs on mount

import { registerPushToken } from '../../api/notifications';

useEffect(() => {
  registerPushToken();
}, []);
```

### Step 4 — Handle incoming notifications (foreground + background)

```javascript
// mobile/app/_layout.jsx  (root layout — runs for all screens)

import { useEffect } from 'react';
import { useRouter } from 'expo-router';
import * as Notifications from 'expo-notifications';

// This controls how notifications look when the app is OPEN
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,   // show banner even when app is open
    shouldPlaySound: true,
    shouldSetBadge:  true,
  }),
});

export default function RootLayout() {
  const router = useRouter();

  useEffect(() => {
    // When user TAPS a notification (app was closed or in background)
    const subscription = Notifications.addNotificationResponseReceivedListener(
      (response) => {
        const data = response.notification.request.content.data;

        // Navigate to alerts screen when notification is tapped
        if (data?.type === 'broadcast') {
          router.push('/alerts');
        }
      }
    );

    return () => subscription.remove();
  }, []);

  // ... rest of your layout
}
```

---

## 5. Setup — Back end (Laravel)

### Step 1 — Install the Laravel Expo package

```bash
cd backend
composer require laravel-notification-channels/expo
```

### Step 2 — Add expo_push_token column to resq_users

Create a new migration:

```bash
php artisan make:migration add_expo_push_token_to_resq_users
```

```php
// database/migrations/xxxx_add_expo_push_token_to_resq_users.php

public function up(): void
{
    Schema::table('resq_users', function (Blueprint $table) {
        // Stores the device's Expo push token
        // Example value: ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]
        $table->string('expo_push_token')->nullable()->after('phone');
    });
}

public function down(): void
{
    Schema::table('resq_users', function (Blueprint $table) {
        $table->dropColumn('expo_push_token');
    });
}
```

```bash
php artisan migrate
```

### Step 3 — API endpoint to save the push token

```php
// routes/api.php
Route::post('/push-tokens', [PushTokenController:REDACTED, 'store'])
    ->middleware('auth:sanctum');
```

```php
// app/Http/Controllers/PushTokenController.php

<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class PushTokenController extends Controller
{
    // Saves the device push token for the logged-in user
    public function store(Request $request)
    {
        $request->validate([
            'token' =REDACTED 'required|string|starts_with:ExponentPushToken',
        ]);

        // Update the token for this user
        $request->user()->update([
            'expo_push_token' =REDACTED $request->token,
        ]);

        return response()->json(['message' => 'Token saved']);
    }
}
```

---

## 6. Sending a Broadcast — the Full Code

This is the core feature. When HQ clicks "Send Broadcast", Laravel:
1. Saves the broadcast to `resq_broadcasts`
2. Finds all target users based on recipient_type and disaster_type
3. Sends push notifications in batches of 100

### BroadcastController.php — send() method

```php
// app/Http/Controllers/Broadcast/BroadcastController.php

<?php

namespace App\Http\Controllers\Broadcast;

use App\Http\Controllers\Controller;
use App\Models\Broadcast;
use App\Models\User;
use App\Models\DisasterEvent;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class BroadcastController extends Controller
{
    // GET /api/broadcasts — list all broadcasts for active event
    public function index()
    {
        $event = DisasterEvent::where('status', 'active')->first();

        if (!$event) {
            return response()->json([]);
        }

        $broadcasts = Broadcast::where('disaster_event_id', $event->id)
            ->with('sender:id,name')
            ->orderBy('created_at', 'desc')
            ->get();

        return response()->json($broadcasts);
    }

    // POST /api/broadcasts — send a new broadcast
    public function send(Request $request)
    {
        $request->validate([
            'disaster_type'  => 'required|string',
            'message'        => 'required|string|min:10',
            'recipient_type' => 'required|in:all,rescuers_only,purok_specific',
            'target_purok'   => 'nullable|string|required_if:recipient_type,purok_specific',
            'priority'       => 'required|in:critical,high,normal',
        ]);

        // Get the active disaster event
        $event = DisasterEvent::where('status', 'active')->first();

        // Save the broadcast record
        $broadcast = Broadcast::create([
            'disaster_event_id' => $event?->id,
            'sent_by'           => $request->user()->id,
            'disaster_type'     => $request->disaster_type,
            'message'           => $request->message,
            'recipient_type'    => $request->recipient_type,
            'target_purok'      => $request->target_purok,
            'priority'          => $request->priority,
        ]);

        // Get the push tokens of target users
        $tokens = $this->getTargetTokens(
            $request->recipient_type,
            $request->disaster_type,
            $request->target_purok
        );

        // Send push notifications if there are any tokens
        if ($tokens->isNotEmpty()) {
            $this->sendPushNotifications(
                $tokens->toArray(),
                $request->disaster_type,
                $request->message,
                $request->priority,
                $broadcast->id
            );
        }

        // Log the action
        \DB::table('resq_activity_logs')->insert([
            'disaster_event_id' => $event?->id,
            'actor_id'          => $request->user()->id,
            'actor_role'        => 'hq_dispatcher',
            'event_type'        => 'broadcast.sent',
            'entity_type'       => 'broadcast',
            'entity_id'         => $broadcast->id,
            'description'       => 'Broadcast sent: ' . $request->disaster_type . ' to ' . $request->recipient_type,
            'created_at'        => now(),
            'updated_at'        => now(),
        ]);

        return response()->json([
            'message'         => 'Broadcast sent',
            'tokens_notified' => $tokens->count(),
            'broadcast'       => $broadcast,
        ]);
    }

    // Decide which users to notify based on disaster type and recipient setting
    private function getTargetTokens(string $recipientType, string $disasterType, ?string $purok)
    {
        $query = User::whereNotNull('expo_push_token')
            ->where('is_active', true);

        if ($recipientType === 'rescuers_only') {
            // Fire and Landslide — notify rescuers only
            $query->where('role', 'rescuer');

        } elseif ($recipientType === 'purok_specific' && $purok) {
            // Specific purok — notify households and rescuers in that purok
            $query->where('purok', $purok);

        } else {
            // all — Typhoon, Flood, Earthquake — notify everyone
            $query->whereIn('role', ['household', 'rescuer']);
        }

        return $query->pluck('expo_push_token');
    }

    // Send notifications in batches of 100 (Expo limit per request)
    private function sendPushNotifications(
        array  $tokens,
        string $disasterType,
        string $message,
        string $priority,
        int    $broadcastId
    ): void {
        // Build the notification payload for each token
        $notifications = array_map(function ($token) use ($disasterType, $message, $priority, $broadcastId) {
            return [
                'to'       => $token,
                'title'    => $this->getAlertTitle($disasterType),
                'body'     => $message,
                'sound'    => 'default',
                'priority' => $priority === 'critical' ? 'high' : 'normal',
                'data'     => [
                    'type'         => 'broadcast',
                    'broadcast_id' => $broadcastId,
                    'disaster'     => $disasterType,
                ],
                // Android notification channel
                'channelId' => 'disaster-alerts',
            ];
        }, $tokens);

        // Expo only accepts 100 notifications per request — split into chunks
        $chunks = array_chunk($notifications, 100);

        foreach ($chunks as $chunk) {
            Http::post('https://exp.host/--/api/v2/push/send', $chunk);
            // Small pause between batches to stay under rate limit
            if (count($chunks) > 1) {
                usleep(200000); // 0.2 seconds
            }
        }
    }

    // Notification title based on disaster type
    private function getAlertTitle(string $type): string
    {
        $titles = [
            'typhoon'    => '🌀 TYPHOON ALERT — ResQperation',
            'flood'      => '🌊 FLOOD ALERT — ResQperation',
            'fire'       => '🔥 FIRE ALERT — ResQperation',
            'earthquake' => '⚠️ EARTHQUAKE ALERT — ResQperation',
            'landslide'  => '⛰️ LANDSLIDE ALERT — ResQperation',
            'other'      => '🚨 EMERGENCY ALERT — ResQperation',
        ];
        return $titles[$type] ?? '🚨 EMERGENCY ALERT — ResQperation';
    }
}
```

---

## 7. Broadcast Rules by Disaster Type

This matches the prototype logic exactly:

```
Typhoon    → send to ALL (households + rescuers) — wide area affected
Flood      → send to ALL (households + rescuers) — wide area affected
Earthquake → send to ALL (households + rescuers) — wide area affected
Fire       → send to RESCUERS ONLY — localized, neighborhood only
Landslide  → send to RESCUERS ONLY — localized, neighborhood only

Purok-specific → send to ALL users in that purok only (overrides above)
```

This is already implemented in `getTargetTokens()` in the controller above.
The `recipient_type` field in the request controls this — the web front end
sets it automatically when the dispatcher picks a disaster type.

---

## 8. Testing Without a Real Device

### Option A — Expo Go app (recommended for capstone)

1. Install **Expo Go** on your Android or iPhone
2. Run `npx expo start` in the mobile folder
3. Scan the QR code
4. Push notifications work on Expo Go — no build required

### Option B — Expo push notification tool

Test sending a notification manually without writing any code:

1. Go to https://expo.dev/notifications
2. Paste in an `ExponentPushToken[...]` from your device
3. Fill in the title and body
4. Click Send — the notification appears on your phone

This is useful for testing before the back end is connected.

### Option C — Test the API directly with Postman

```
POST https://exp.host/--/api/v2/push/send
Content-Type: application/json

{
  "to": "ExponentPushToken[your_token_here]",
  "title": "🌀 TYPHOON ALERT — ResQperation",
  "body": "Typhoon Caloy Signal No. 2. Proceed to nearest evacuation center.",
  "sound": "default",
  "priority": "high",
  "data": { "type": "broadcast", "disaster": "typhoon" }
}
```

---

## 9. Common Errors and Fixes

| Error | What it means | Fix |
|---|---|---|
| `DeviceNotRegistered` | Token is stale — user uninstalled the app | Set `expo_push_token = REDACTED for that user when you get this error |
| `InvalidCredentials` | Wrong Expo access token | Check `EXPO_ACCESS_TOKEN` in `.env` — or remove it (token is optional for free use) |
| `MessageTooBig` | Notification body over 4KB | Keep message short — disaster alerts should be under 200 characters |
| `ExponentPushToken[...]` not saving | registerPushToken called before permission granted | Make sure `requestPermissionsAsync()` resolves before `getExpoPushTokenAsync()` |
| Notification not showing on Android | Missing notification channel | Add `channelId: 'disaster-alerts'` to payload AND create the channel in the app |
| Works in Expo Go but not in APK | Project ID missing | Add `projectId` in `getExpoPushTokenAsync({ projectId: 'your-id' })` |

### Create Android notification channel (required for Android 8+)

Add this once when the app starts, in `mobile/app/_layout.jsx`:

```javascript
import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Create the disaster-alerts channel for Android
if (Platform.OS === 'android') {
  Notifications.setNotificationChannelAsync('disaster-alerts', {
    name:                  'Disaster Alerts',
    importance:            Notifications.AndroidImportance.MAX,
    vibrationPattern:      [0, 250, 250, 250],
    lightColor:            '#DC2626',  // red
    lockscreenVisibility:  Notifications.AndroidNotificationVisibility.PUBLIC,
    bypassDnd:             true,  // bypass Do Not Disturb for emergencies
  });
}
```

---

## Summary — What you need to do

```
1. Mobile setup
   ├── npx expo install expo-notifications expo-device
   ├── Call registerPushToken() after login
   ├── Set up notification handler in _layout.jsx
   └── Create Android notification channel

2. Back end setup
   ├── composer require laravel-notification-channels/expo
   ├── Add expo_push_token column to resq_users → php artisan migrate
   ├── Add POST /api/push-tokens route + PushTokenController
   └── Add send() method in BroadcastController (code above)

3. No external accounts needed for basic use
   └── Optional: create free Expo account at expo.dev
       to get an access token for extra security
```

---

## Environment Variables

```env
# backend/.env
# Only needed if you want extra security on the Expo push API
# Leave empty for capstone — works fine without it
EXPO_ACCESS_TOKEN=
REDACTED

```env
# mobile/.env  (or hardcode projectId in app.json)
EXPO_PROJECT_ID=your-project-id-from-expo-dashboard
```

---

## Related Files in This Repo

```
backend/
├── app/Http/Controllers/Broadcast/BroadcastController.php  ← send() method here
├── app/Http/Controllers/PushTokenController.php            ← saves device token
└── database/migrations/xxxx_add_expo_push_token_to_resq_users.php

mobile/
├── api/notifications.js        ← registerPushToken() function
├── app/_layout.jsx             ← notification handler + Android channel
├── app/(household)/home.jsx    ← calls registerPushToken on mount
└── app/(rescuer)/home.jsx      ← calls registerPushToken on mount
```

---

*ResQperation — Barangay Disaster Risk Reduction and Management System*
*Associate Degree in Software Development Capstone Project*
