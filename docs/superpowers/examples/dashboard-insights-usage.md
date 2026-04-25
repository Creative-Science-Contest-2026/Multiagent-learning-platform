# Dashboard Insights — Quick Frontend Usage (T050)

This short example shows how to call the new `GET /api/v1/dashboard/insights` endpoint
from the frontend using the existing client helper `getDashboardInsights()` in
`web/lib/dashboard-api.ts`.

Client-side React (Next.js) example:

```tsx
import React, { useEffect, useState } from "react";
import { getDashboardInsights, DashboardInsights } from "@/lib/dashboard-api";

export default function DashboardInsightsExample() {
  const [insights, setInsights] = useState<DashboardInsights | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getDashboardInsights(100);
        setInsights(data);
      } catch (err) {
        console.error("Failed to load dashboard insights", err);
      }
    })();
  }, []);

  if (!insights) return <div>Loading insights…</div>;

  return (
    <div>
      <h2>Analytics</h2>
      <pre>{JSON.stringify(insights.analytics, null, 2)}</pre>

      <h3>At-risk topics</h3>
      <pre>{JSON.stringify(insights.at_risk_topics, null, 2)}</pre>

      <h3>Recommendations</h3>
      <ul>
        {insights.recommendations.map((r) => (
          <li key={r}>{r}</li>
        ))}
      </ul>
    </div>
  );
}
```

Notes:

- This example uses the TypeScript client `getDashboardInsights()` added in T050.
- Place this component in a convenient UI location or use it as a quick dev/debug page.
- The example is intentionally small: production placement and styling should be
  handled by Lane 1 if the UI exposure is requested.
