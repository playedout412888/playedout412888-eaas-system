# Quick Start Guide

## 🚀 Commands

```bash
# Development
npm run dev              # Start dev server at localhost:3000

# Quality Checks
npm run lint             # ESLint
npm run type-check       # TypeScript
npm run test             # Jest tests
npm run test:coverage    # Coverage report

# Production
npm run build            # Build for production
npm start                # Start production server

# Deployment
git push origin main     # Triggers Vercel deploy
```

---

## 🔧 Setup

### 1. Environment Variables
```bash
cp .env.example .env.local
# Edit with your values:
# NEXT_PUBLIC_SUPABASE_URL
# NEXT_PUBLIC_SUPABASE_ANON_KEY
# OPENAI_API_KEY
# E2B_API_KEY
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development
```bash
npm run dev
# Open http://localhost:3000
```

---

## 📚 Documentation

| File | Purpose |
|------|----------|
| [README.md](./README.md) | Project overview |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Development guide |
| [docs/API.md](./docs/API.md) | API reference |
| [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System design |
| [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md) | Detailed setup |
| [DEPLOY.md](./DEPLOY.md) | Quick deploy guide |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

---

## 🎯 Workflow

1. Create feature branch
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make changes and commit
   ```bash
   git commit -m "feat: description"
   ```

3. Push and create PR
   ```bash
   git push origin feature/my-feature
   ```

4. Merge to main
   ```bash
   # GitHub: Click merge
   ```

5. Auto-deploy to Vercel
   ```bash
   # Automatic! ✅
   ```

---

## 🔗 Useful Links

- **GitHub**: https://github.com/playedout412888/playedout412888-eaas-system
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Supabase Console**: https://app.supabase.io
- **OpenAI API**: https://platform.openai.com
- **E2B Dashboard**: https://e2b.dev/dashboard

---

**Happy coding! 🚀**