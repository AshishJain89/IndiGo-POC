import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { 
  Calendar, 
  Users, 
  Plane, 
  BarChart3,
  Home,
  MessageSquare
} from "lucide-react";

interface NavigationProps {
  activeView: string;
  onViewChange: (view: string) => void;
}

const navigationItems = [
  { id: "dashboard", label: "Dashboard", icon: Home },
  { id: "crew", label: "Crew", icon: Users },
  { id: "flights", label: "Flights", icon: Plane },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
];

export function Navigation({ activeView, onViewChange }: NavigationProps) {
  return (
    <nav className="w-64 bg-card border-r border-border h-full flex flex-col">
      <div className="p-4">
        <div className="space-y-2">
          {navigationItems.map((item) => (
            <Button
              key={item.id}
              variant={activeView === item.id ? "default" : "ghost"}
              className={cn(
                "w-full justify-start gap-3",
                activeView === item.id && "bg-primary text-primary-foreground"
              )}
              onClick={() => onViewChange(item.id)}
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </Button>
          ))}
        </div>
      </div>
      
      <div className="mt-auto p-4 border-t border-border">
        <Button variant="outline" className="w-full gap-2">
          <MessageSquare className="h-4 w-4" />
          AI Assistant
        </Button>
      </div>
    </nav>
  );
}