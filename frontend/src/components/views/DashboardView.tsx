import { RosterView } from "@/components/dashboard/RosterView";
import { DisruptionsPanel } from "@/components/dashboard/DisruptionsPanel";
import { CompliancePanel } from "@/components/dashboard/CompliancePanel";
import { ConflictsPane } from "@/components/dashboard/ConflictsPane";
import { ChatAssistant } from "@/components/chat/ChatAssistant";

export function DashboardView() {
  return (
    <div className="flex h-full gap-6 p-6">
      {/* Main Dashboard Content */}
      <div className="flex-1 space-y-6 max-w-5xl w-full">
        {/* Top Row - Roster View */}
        <RosterView />
        
        {/* Middle Row - Disruptions and Compliance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <DisruptionsPanel />
          <CompliancePanel />
        </div>
        
        {/* Bottom Row - Conflicts */}
        <ConflictsPane />
      </div>
      
      {/* Right Sidebar - Chat Assistant */}
      <div className="w-96 flex-shrink-0">
        <ChatAssistant />
      </div>
    </div>
  );
}