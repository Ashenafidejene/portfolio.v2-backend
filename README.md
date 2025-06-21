# AI Portfolio Backend with Firebase

🔥 FastAPI backend with Firebase integration for authentication and real-time data

## Key Features

- **Firebase Integration**:
  - Google Authentication (Sign-in with Google)
  - Realtime Database for comments/likes
  - Serverless architecture ready
- **Multi-LLM Gateway** (Gemini, ChatGPT, DeepSeek)
- **Secure API Endpoints** with JWT verification

## Firebase Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project" and follow the wizard

### 2. Set Up Authentication
```bash
# Enable Google Auth Provider:
1. Go to Authentication → Sign-in method
2. Enable "Google" provider
3. Add your domain to authorized domains
```
### 3. Get Service Account Key
```bash
1. Project Settings → Service Accounts
2. Generate new private key (JSON)
3. Save as `firebase-key.json` in project root
```
### Configuration
Update .env:

```bash
DEEPSEEK_API_KEY=
GEMINI_API_KEY=
OPENAI_API_KEY=
FIREBASE_CREDENTIALS_PATH=
FIREBASE_DATABASE_URL=
```
### Authentication Flow
['./images/deepseek_mermaid_20250621_aa9cc1.png']
