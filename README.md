# HORT 2000 — Tomato Decision Lab

A Streamlit classroom companion for **The $25,000 Tomato Decision**. Includes a pre-decision prediction, an adjustable economic sensitivity model, links to four separate Google Gemini Gems, and a rule-based decision review with CSV export.

**Important:** This is not a live pest-management recommendation, a Gemini API connection, or an AI grading system. Stakeholder conversations open in external Gemini tabs. Farm economics, pest losses, strategy costs, and efficacies are teaching assumptions.

## Local run

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Community Cloud / GitHub

1. Create a new GitHub repository, e.g. `hort-2000-tomato-decision`.
2. Upload **both** `app.py` and `requirements.txt` to the root of that repository. Commit changes.
3. Visit https://share.streamlit.io and select **Create app** / **Deploy an app**.
4. Choose your GitHub repository and branch; set main file to `app.py`.
5. Deploy, then test the app and Gem links from a participant account.
6. Distribute the resulting `.streamlit.app` address (or generate a QR code for it).

If you already have a deployed Streamlit app from a different GitHub repo, use a new repo or a separate entrypoint rather than overwriting that project.

## Model

`Gross revenue = acres * yield(lb/acre) * $/lb`

`Revenue at risk = gross revenue * no-intervention-loss%`

`Preserved revenue = revenue at risk * prevented-loss%`

`Net benefit = preserved revenue - strategy cost`

There is no claim of agronomic forecasting accuracy or biological validation.

## References

- UGA CAES Commercial Tomato Production Handbook (B1312, reviewed 2017): https://fieldreport.caes.uga.edu/publications/B1312/commercial-tomato-production-handbook/
- Streamlit deployment docs: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
