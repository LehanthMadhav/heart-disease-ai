
import { Activity, BrainCircuit } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { PageShell } from "@/components/dashboard/page-shell";

export default function AnalyticsPage() {
  return (
    <PageShell
      title="Model Analytics"
      description="Machine learning model evaluation and performance monitoring."
    >
      <Badge variant="outline">Awaiting cloud training</Badge>

      <div className="grid gap-5 md:grid-cols-2">
        <Card>
          <CardContent className="p-6">
            <BrainCircuit className="text-blue-600" size={26} />

            <h2 className="mt-4 font-semibold">
              Model Comparison
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Logistic Regression, Decision Tree and Random Forest
              comparisons will appear here after training.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <Activity className="text-blue-600" size={26} />

            <h2 className="mt-4 font-semibold">
              Evaluation Metrics
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Precision, recall, specificity, F1-score and ROC-AUC
              will be displayed using actual experimental results.
            </p>
          </CardContent>
        </Card>
      </div>
    </PageShell>
  );
}
