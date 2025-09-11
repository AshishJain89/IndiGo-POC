import { useState } from "react";
import { DashboardHeader } from "@/components/layout/DashboardHeader";
import { AppSidebar } from "@/components/layout/AppSidebar";
import { DashboardView } from "@/components/views/DashboardView";
import { CrewView } from "@/components/views/CrewView";
import { FlightView } from "@/components/views/FlightView";
import { AnalyticsView } from "@/components/views/AnalyticsView";
import { ChatAssistant } from "@/components/chat/ChatAssistant";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";

export function CrewRosterDashboard() {
  const [activeView, setActiveView] = useState("dashboard");
  const [showChat, setShowChat] = useState(false);

  const renderActiveView = () => {
    switch (activeView) {
      case "crew":
        return <CrewView />;
      case "flights":
        return <FlightView />;
      case "analytics":
        return <AnalyticsView />;
      default:
        return <DashboardView />;
    }
  };

  return (
    <SidebarProvider>
      <div className="h-screen flex flex-col bg-background w-full min-w-0">
      {/* Header row, not inside sidebar/content flex */}
      <header className="h-16 px-4 border-b border-border bg-card shadow-sm flex items-center min-w-0">
        <SidebarTrigger className="mr-4" />
        <div className="flex-1">
          <DashboardHeader />
        </div>
      </header>
      {/* Sidebar/content row */}
      <div className="flex flex-1 min-h-0 overflow-hidden min-w-0 w-full">
        <AppSidebar 
          activeView={activeView} 
          onViewChange={setActiveView}
          onChatToggle={() => setShowChat(!showChat)}
        />
        <div className="flex flex-1 min-w-0 w-full overflow-hidden">
          <main className="flex-1 min-w-0 w-full overflow-auto">
            {renderActiveView()}
          </main>
          {showChat && (
            <div className="w-96 min-w-[24rem] max-w-[100vw] border-l border-border bg-card shadow-lg overflow-auto flex-shrink-0">
              <ChatAssistant onClose={() => setShowChat(false)} />
            </div>
          )}
        </div>
      </div>
    </div>
    </SidebarProvider>
  );
}