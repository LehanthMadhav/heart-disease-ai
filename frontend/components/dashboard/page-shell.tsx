
import type { ReactNode } from "react";
import { Sidebar } from "./sidebar";
import { Header } from "./header";

interface PageShellProps {
  title: string;
  description: string;
  children: ReactNode;
}

export function PageShell({
  title,
  description,
  children,
}: PageShellProps) {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />

      <main className="min-w-0 flex-1">
        <Header />

        <div className="space-y-8 p-8">
          <section>
            <h1 className="text-2xl font-bold text-slate-900">
              {title}
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              {description}
            </p>
          </section>

          {children}
        </div>
      </main>
    </div>
  );
}
