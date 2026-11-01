
import { Bell, Search } from "lucide-react";

export function Header() {
  return (
    <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-8">
      <div>
        <h2 className="text-lg font-semibold text-slate-900">
          Dashboard Overview
        </h2>
        <p className="text-sm text-slate-500">
          Welcome to your clinical analytics workspace.
        </p>
      </div>

      <div className="flex items-center gap-5">
        <div className="hidden items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 md:flex">
          <Search size={17} className="text-slate-400" />
          <input
            type="text"
            placeholder="Search..."
            className="w-36 bg-transparent text-sm outline-none"
          />
        </div>

        <button
          type="button"
          aria-label="Notifications"
          className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
        >
          <Bell size={20} />
        </button>

        <div className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
          ML
        </div>
      </div>
    </header>
  );
}
