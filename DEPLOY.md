# Deployment Quick Start

## 🚀 Deploy Your App in Minutes

### Option 1: Vercel (Recommended)

```bash
# 1. Connect to Vercel
# Visit: https://vercel.com/new
# Select your GitHub repo
# Vercel auto-detects Next.js
# Add env variables
# Deploy!

# 2. Automatic deploys on push
git push origin main
```

### Option 2: Docker

```bash
docker build -t ai-platform:latest .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_SUPABASE_URL=your_url \
  -e OPENAI_API_KEY=sk-... \
  ai-platform:latest
```

---

## ✅ Deployment Checklist

- [ ] All tests pass: `npm run test`
- [ ] No lint errors: `npm run lint`
- [ ] Type check passes: `npm run type-check`
- [ ] Build succeeds: `npm run build`
- [ ] Environment variables configured
- [ ] Database schema created
- [ ] API keys secured
- [ ] README updated
- [ ] CHANGELOG updated

---

## 🔐 Security Checklist

- [ ] No .env files in git
- [ ] Dependencies audited: `npm audit`
- [ ] Secrets in Vercel, not code
- [ ] Branch protection enabled
- [ ] Status checks required

---

## 📊 Your Deploy URLs

| Environment | URL | Status |
|---|---|---|
| Production | https://your-domain.vercel.app | Ready! |
| Preview | Auto on PR | Ready! |

---

## 🔧 Troubleshooting

### Build Fails
```bash
# Test locally
npm run build

# Check logs
vercel logs --follow
```

### Runtime Error
```bash
# View logs
vercel logs --follow

# Check env vars in Vercel dashboard
```

---

**Ready to deploy? Push to main! 🎉**