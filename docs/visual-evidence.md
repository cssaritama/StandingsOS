# Visual evidence checklist

The README should show the real product, not a generated mockup.

After starting the current release with Docker Compose, capture the following from the running application:

1. **Hero / competition overview**
   - competition and season selectors visible;
   - standings and metric cards in the same frame where possible.

2. **AI-ready data panel**
   - readiness score;
   - dimension-level scores;
   - blockers or warnings, if present.

3. **Fixtures and results**
   - at least one completed fixture and one scheduled fixture.

4. **Forecasts**
   - transparent home/draw/away probabilities.

5. **Evidence-grounded AI**
   - only if the optional provider is enabled;
   - include the readiness gate and bounded evidence behavior.

6. **Azure / deployment evidence**
   - only after a real Azure validation;
   - sanitized AKS / ACR / Azure Monitor screenshots;
   - never include subscription IDs, secrets, private hostnames or credentials.

Recommended filenames:

```text
docs/assets/hero-dashboard.png
docs/assets/data-readiness.png
docs/assets/fixtures-results.png
docs/assets/forecasts.png
docs/assets/ai-evidence.png
docs/assets/azure-validation.png
docs/assets/demo.gif
```

## README rule

Do not add an image reference to the README until the corresponding real file exists.

## GIF sequence

A useful 10–20 second demo:

```text
open seeded competition
  -> inspect standings
  -> record / inspect result
  -> see derived standings update
  -> inspect AI-readiness score
  -> inspect forecasts
  -> open evidence brief (if enabled)
```

The point is to prove the product workflow, not to create a cinematic marketing video.
