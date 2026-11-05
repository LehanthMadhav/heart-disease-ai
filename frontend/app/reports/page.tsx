
import { FileText, Database } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { PageShell } from "@/components/dashboard/page-shell";

export default function ReportsPage() {
  return (
    <PageShell
      title="Prediction Reports"
      description="Research reports and model evaluation summaries."
    >
      <Card>
        <CardContent className="flex flex-col items-center p-12 text-center">
          <div className="rounded-full bg-blue-50 p-4">
            <FileText size={30} className="text-blue-600" />
          </div>

          <h2 className="mt-5 font-semibold text-slate-900">
            No reports available
          </h2>

          <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">
            Reports will become available after the machine learning
            pipeline has been trained and evaluated.
          </p>

          <Database size={20} className="mt-6 text-slate-400" />
        </CardContent>
      </Card>
    </PageShell>
  );
}
