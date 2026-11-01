
import {
  Activity,
  Users,
  BrainCircuit,
  ShieldCheck,
  ArrowUpRight,
  Clock3,
} from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sidebar } from "@/components/dashboard/sidebar";
import { Header } from "@/components/dashboard/header";

const statistics = [
  {
    title: "Patients Assessed",
    value: "—",
    description: "Awaiting dataset integration",
    icon: Users,
  },
  {
    title: "Active ML Models",
    value: "0",
    description: "No trained model connected",
    icon: BrainCircuit,
  },
  {
    title: "Model Performance",
    value: "—",
    description: "Evaluation pending",
    icon: Activity,
  },
  {
    title: "Validation Status",
    value: "Pending",
    description: "Clinical validation not performed",
    icon: ShieldCheck,
  },
];

export default function DashboardPage() {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />

      <main className="min-w-0 flex-1">
        <Header />

        <div className="space-y-8 p-8">
          <section className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-slate-900">
                Heart Disease AI
              </h1>
              <p className="mt-1 text-sm text-slate-500">
                Clinical data analytics and machine learning workspace.
              </p>
            </div>

            <Badge className="bg-amber-100 px-3 py-1 text-amber-800 hover:bg-amber-100">
              DEMO ENVIRONMENT
            </Badge>
          </section>

          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {statistics.map((item) => {
              const Icon = item.icon;

              return (
                <Card key={item.title} className="border-slate-200 shadow-sm">
                  <CardContent className="p-5">
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-slate-500">
                        {item.title}
                      </p>
                      <div className="rounded-lg bg-blue-50 p-2 text-blue-600">
                        <Icon size={19} />
                      </div>
                    </div>

                    <h3 className="mt-4 text-2xl font-bold text-slate-900">
                      {item.value}
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      {item.description}
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </section>

          <section className="grid gap-6 xl:grid-cols-3">
            <Card className="border-slate-200 shadow-sm xl:col-span-2">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-slate-900">
                      Model Development
                    </h3>
                    <p className="mt-1 text-sm text-slate-500">
                      Progress of the machine learning pipeline.
                    </p>
                  </div>

                  <BrainCircuit className="text-blue-600" size={24} />
                </div>

                <div className="mt-8 space-y-5">
                  {[
                    "Dataset preparation",
                    "Data preprocessing",
                    "Model training",
                    "Model evaluation",
                    "API integration",
                  ].map((step, index) => (
                    <div key={step} className="flex items-center gap-3">
                      <div className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-sm font-semibold text-slate-500">
                        {index + 1}
                      </div>

                      <p className="text-sm text-slate-700">{step}</p>

                      <span className="ml-auto text-xs text-slate-400">
                        Not started
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-slate-200 shadow-sm">
              <CardContent className="p-6">
                <div className="flex items-center gap-2">
                  <Clock3 size={20} className="text-blue-600" />
                  <h3 className="font-semibold text-slate-900">
                    Recent Activity
                  </h3>
                </div>

                <div className="mt-6 rounded-lg bg-slate-50 p-4">
                  <p className="text-sm font-medium text-slate-800">
                    Project workspace created
                  </p>
                  <p className="mt-2 text-xs text-slate-500">
                    Initial frontend and backend environment setup.
                  </p>
                  <p className="mt-3 text-xs text-emerald-700">
                    <ArrowUpRight className="mr-1 inline" size={14} />
                    Development started
                  </p>
                </div>

                <p className="mt-5 text-xs leading-5 text-slate-500">
                  This section will display actual project events once
                  application activity tracking is implemented.
                </p>
              </CardContent>
            </Card>
          </section>

          <footer className="border-t border-slate-200 pt-5 text-xs leading-5 text-slate-500">
            Academic research prototype. This application is not a medical
            diagnostic tool and must not be used for clinical decisions.
          </footer>
        </div>
      </main>
    </div>
  );
}
