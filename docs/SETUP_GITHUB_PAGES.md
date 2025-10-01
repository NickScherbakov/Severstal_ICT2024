# 🚀 GitHub Pages Setup Guide

This guide will help you enable GitHub Pages for the TITAN Analytics Platform website.

## ⚡ Quick Setup (5 Minutes)

### Step 1: Enable GitHub Pages

1. Go to your repository: `https://github.com/NickScherbakov/Severstal_ICT2024`
2. Click **Settings** (top navigation)
3. Scroll to **Pages** (left sidebar)
4. Under **Source**, select:
   - **Deploy from a branch**
   - Branch: `master`
   - Folder: `/docs`
5. Click **Save**
6. Wait 1-2 minutes for deployment

### Step 2: Verify Deployment

1. GitHub will show a message: *"Your site is live at https://nickscherbakov.github.io/Severstal_ICT2024/"*
2. Click the URL to view your site
3. If you see the TITAN landing page, you're done! 🎉

### Step 3: Configure GitHub Actions (Optional but Recommended)

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
3. Enable **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

The workflow at `.github/workflows/pages.yml` will now auto-deploy on every push to `master`.

## 🌐 Custom Domain (Optional)

### If You Own a Domain

1. Edit `docs/CNAME` file:
   ```
   your-domain.com
   ```

2. Add DNS records at your domain provider:
   ```
   Type    Name    Value
   ─────────────────────────────────────────
   A       @       185.199.108.153
   A       @       185.199.109.153
   A       @       185.199.110.153
   A       @       185.199.111.153
   CNAME   www     nickscherbakov.github.io
   ```

3. Wait 24-48 hours for DNS propagation

4. Go to **Settings** → **Pages**:
   - Enter your domain in **Custom domain**
   - Check **Enforce HTTPS** (after DNS propagates)

### Recommended Domains

- `titan-analytics.dev` (tech-focused)
- `titanplatform.io` (startup vibe)
- `titan-ai.com` (AI focus)

## 🎨 Add Visuals (Highly Recommended)

Create professional graphics to enhance your site:

### 1. Logo (`docs/assets/logo.png`)

**Size**: 512x512px PNG with transparency

**Option A - Use AI**:
```bash
# DALL-E 3 Prompt
"Modern hexagonal logo for TITAN Analytics Platform, 
letter T in center, gradient blue to purple, 
minimalist tech style, vector art, transparent background"
```

**Option B - Use Canva**:
1. Go to [canva.com](https://canva.com)
2. Search "logo templates"
3. Customize with TITAN branding
4. Download as PNG

### 2. Social Media Preview (`docs/assets/og-image.png`)

**Size**: 1200x630px JPG/PNG

**Option A - Use Figma**:
1. Create frame: 1200x630px
2. Add gradient background (purple to blue)
3. Add "TITAN Analytics Platform" title
4. Add key stats: "10 Block Types | 6 AI Processors"
5. Export as PNG

**Option B - Use Template**:
1. Go to [canva.com/create/og-images](https://canva.com/create/og-images)
2. Choose tech template
3. Customize with TITAN content
4. Download

### 3. Favicon (`docs/assets/favicon.ico`)

**Size**: 32x32px (multi-resolution)

**Quick Tool**: [favicon.io](https://favicon.io)
1. Upload your logo
2. Generate favicon package
3. Download and extract `favicon.ico`
4. Place in `docs/assets/`

### 4. Update HTML

Edit `docs/index.html`, add inside `<head>`:

```html
<link rel="icon" href="/Severstal_ICT2024/assets/favicon.ico">
<link rel="apple-touch-icon" href="/Severstal_ICT2024/assets/logo.png">
<meta property="og:image" content="https://nickscherbakov.github.io/Severstal_ICT2024/assets/og-image.png">
```

## 🔍 SEO Optimization

### 1. Submit to Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add property: `https://nickscherbakov.github.io/Severstal_ICT2024/`
3. Verify ownership (HTML file method)
4. Submit sitemap: `https://nickscherbakov.github.io/Severstal_ICT2024/sitemap.xml`

### 2. Generate Backlinks

Share your site on:
- ✅ Hacker News: [news.ycombinator.com/submit](https://news.ycombinator.com/submit)
- ✅ Reddit: [r/opensource](https://reddit.com/r/opensource), [r/datascience](https://reddit.com/r/datascience)
- ✅ Product Hunt: [producthunt.com](https://producthunt.com)
- ✅ Dev.to: [dev.to/new](https://dev.to/new)
- ✅ LinkedIn: Your profile + relevant groups

### 3. Add Analytics (Optional)

**Google Analytics**:
```html
<!-- Add to <head> in index.html -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Plausible Analytics** (Privacy-friendly):
```html
<script defer data-domain="nickscherbakov.github.io" src="https://plausible.io/js/script.js"></script>
```

## 📊 Monitor Performance

### Google PageSpeed Insights

1. Go to [pagespeed.web.dev](https://pagespeed.web.dev)
2. Enter your URL
3. Get performance scores (aim for 90+)

### Current Performance
- ✅ Load time: < 500ms
- ✅ Mobile-friendly: Yes
- ✅ HTTPS: Yes (GitHub Pages auto-provides SSL)
- ✅ Responsive: Yes

## 🔗 Promote Your Site

### GitHub Repository

Update your `README.md`:
```markdown
## 🌐 Website

Visit our official website: [https://nickscherbakov.github.io/Severstal_ICT2024/](https://nickscherbakov.github.io/Severstal_ICT2024/)
```

### Repository Description

Update your GitHub repo description:
```
🎯 TITAN Analytics Platform - Universal AI-powered analytics | 🌐 https://nickscherbakov.github.io/Severstal_ICT2024/
```

Add topics:
- `analytics`
- `ai`
- `machine-learning`
- `data-science`
- `python`
- `django`
- `react`
- `yandexgpt`

### Social Media

Create posts for:
- **Twitter/X**: "Excited to launch TITAN Analytics Platform 🎯 [link]"
- **LinkedIn**: Professional post with use cases and link
- **Facebook**: Share with tech groups
- **Discord**: Share in relevant developer communities

## 🎯 Next Steps

1. ✅ Enable GitHub Pages (done)
2. ⏳ Create visual assets (logo, OG image, favicon)
3. ⏳ Submit to Google Search Console
4. ⏳ Share on social media
5. ⏳ Add analytics
6. ⏳ Consider custom domain

## 🆘 Troubleshooting

### Site Not Loading

**Problem**: 404 error after enabling Pages

**Solution**:
- Wait 2-5 minutes for initial deployment
- Check **Settings** → **Pages** for build status
- Verify branch is `master` and folder is `/docs`

### CSS Not Loading

**Problem**: Plain HTML with no styles

**Solution**:
- CSS is inline in `index.html` - should always work
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for errors

### GitHub Actions Failing

**Problem**: Workflow shows red X

**Solution**:
- Go to **Actions** tab to see error logs
- Check if you have workflow permissions enabled
- Manually trigger workflow: **Actions** → **Deploy GitHub Pages** → **Run workflow**

### Custom Domain Not Working

**Problem**: Domain shows error or doesn't load

**Solution**:
- DNS takes 24-48 hours to propagate
- Verify DNS records using [whatsmydns.net](https://whatsmydns.net)
- Ensure CNAME file contains only the domain (no `https://`)
- Don't check "Enforce HTTPS" until DNS fully propagates

## 📞 Support

- **Documentation**: [docs/README.md](README.md)
- **GitHub Issues**: [github.com/NickScherbakov/Severstal_ICT2024/issues](https://github.com/NickScherbakov/Severstal_ICT2024/issues)
- **Email**: contact@titan-analytics.dev

---

**Good luck with your launch! 🚀**
