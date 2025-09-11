import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Bell, Settings, User, Plane } from "lucide-react";
import { ThemeToggle } from "@/components/theme/ThemeToggle";

export function DashboardHeader() {
  return (
    <header className="h-16 bg-card border-b border-border flex items-center justify-between px-6 sticky top-0 z-50 shadow-sm">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <Plane className="h-8 w-8 text-primary" />
          <h1 className="text-2xl font-bold text-foreground">CrewRoster AI</h1>
        </div>
        <Badge variant="outline" className="text-xs">
          Pro Dashboard
        </Badge>
      </div>
      
      <div className="flex items-center gap-2">
        <ThemeToggle />
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="h-5 w-5" />
          <Badge className="absolute -top-1 -right-1 h-5 w-5 rounded-full p-0 flex items-center justify-center text-xs bg-destructive">
            3
          </Badge>
        </Button>
        <Button variant="ghost" size="icon">
          <Settings className="h-5 w-5" />
        </Button>
        <Button variant="ghost" size="icon">
          <User className="h-5 w-5" />
        </Button>
      </div>
    </header>
  );
}