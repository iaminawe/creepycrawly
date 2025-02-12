"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { CrawlConfigForm } from "@/components/CrawlConfigForm";
import { CrawlStatus } from "@/components/CrawlStatus";
import { RecentContent } from "@/components/RecentContent";
import { ConfigForm } from "@/components/ConfigForm";

export default function Home() {
  return (
    <SidebarProvider>
      <div className="flex">
        <AppSidebar />
        <main className="flex-1 p-8">
          <h1 className="text-2xl font-bold">Welcome to the Dashboard</h1>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <CrawlConfigForm />
            <CrawlStatus />
            <ConfigForm />
          </div>
          <RecentContent />
        </main>
      </div>
    </SidebarProvider>
  );
}
