import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { 
  Calendar, 
  CalendarDays, 
  CalendarRange,
  RefreshCw,
  Download,
  Clock,
  Users
} from "lucide-react";
import { format, isSameDay, isSameWeek, isSameMonth, parseISO } from "date-fns";

type ViewMode = "day" | "week" | "month";

interface Assignment {
  id: string;
  flight: string;
  status: string;
  duty_start: Date;
  duty_end: Date;
}
interface CrewRoster {
  crew_id: string;
  name: string;
  role: string;
  assignments: Assignment[];
}

interface CrewMember {
  id: string;
  name: string;
  role: "captain" | "first-officer" | "flight-attendant";
  status: "active" | "standby" | "rest";
  flight?: string;
}

// Add this utility for hiding scrollbars
const hideScrollbar = {
  scrollbarWidth: 'none',
  msOverflowStyle: 'none',
  '::-webkit-scrollbar': { display: 'none' },
};

export function RosterView() {
  const [viewMode, setViewMode] = useState<ViewMode>("day");
  const [isRegenerating, setIsRegenerating] = useState(false);
  const [crewRosters, setCrewRosters] = useState<CrewRoster[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());

  useEffect(() => {
    setLoading(true);
    fetch("/api/rosters/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch roster");
        return res.json();
      })
      .then((data) => {
        // Group by crew
        const grouped: { [crew_id: string]: CrewRoster } = {};
        data.forEach((r: any) => {
          const crew_id = String(r.crew_id);
          if (!grouped[crew_id]) {
            grouped[crew_id] = {
              crew_id,
              name: r.crew_id ? `Crew #${r.crew_id}` : "Unknown",
              role: r.crew_position?.toLowerCase().replace('_', '-') || '',
              assignments: [],
            };
          }
          grouped[crew_id].assignments.push({
            id: String(r.id),
            flight: r.flight_id ? `UA${r.flight_id}` : undefined,
            status: r.status?.toLowerCase() || '',
            duty_start: r.duty_start ? new Date(r.duty_start) : null,
            duty_end: r.duty_end ? new Date(r.duty_end) : null,
          });
        });
        setCrewRosters(Object.values(grouped));
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  // Filtering logic
  function filterAssignments(assignments: Assignment[]): Assignment[] {
    if (viewMode === "day") {
      return assignments.filter(a => a.duty_start && isSameDay(a.duty_start, selectedDate));
    } else if (viewMode === "week") {
      return assignments.filter(a => a.duty_start && isSameWeek(a.duty_start, selectedDate, { weekStartsOn: 1 }));
    } else if (viewMode === "month") {
      return assignments.filter(a => a.duty_start && isSameMonth(a.duty_start, selectedDate));
    }
    return assignments;
  }

  const handleRegenerate = async () => {
    setIsRegenerating(true);
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    setIsRegenerating(false);
  };

  const getCrewColor = (role: string) => {
    switch (role) {
      case "captain": return "bg-crew-captain text-white";
      case "first-officer": return "bg-crew-first-officer text-white";
      case "flight-attendant": return "bg-crew-flight-attendant text-white";
      default: return "bg-muted text-muted-foreground";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active": return "bg-success text-success-foreground";
      case "standby": return "bg-warning text-warning-foreground";
      case "rest": return "bg-muted text-muted-foreground";
      default: return "bg-muted text-muted-foreground";
    }
  };

  // Set a max number of badges to show per row
  const MAX_BADGES = 6;

  return (
    <Card className="shadow-lg w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Roster Overview
          </CardTitle>
          
          <div className="flex items-center gap-2">
            <input
              type="date"
              className="border rounded px-2 py-1 text-xs bg-card text-foreground border-border focus:ring-2 focus:ring-primary focus:outline-none transition-colors duration-150"
              value={format(selectedDate, 'yyyy-MM-dd')}
              onChange={e => setSelectedDate(new Date(e.target.value))}
              disabled={loading}
            />
            <div className="flex rounded-lg border border-border p-1">
              <Button
                variant={viewMode === "day" ? "default" : "ghost"}
                size="sm"
                onClick={() => setViewMode("day")}
                className="px-3"
              >
                <Clock className="h-4 w-4 mr-1" />
                Day
              </Button>
              <Button
                variant={viewMode === "week" ? "default" : "ghost"}
                size="sm"
                onClick={() => setViewMode("week")}
                className="px-3"
              >
                <CalendarDays className="h-4 w-4 mr-1" />
                Week
              </Button>
              <Button
                variant={viewMode === "month" ? "default" : "ghost"}
                size="sm"
                onClick={() => setViewMode("month")}
                className="px-3"
              >
                <CalendarRange className="h-4 w-4 mr-1" />
                Month
              </Button>
            </div>
            
            <Button 
              onClick={handleRegenerate}
              disabled={isRegenerating}
              className="gap-2"
            >
              <RefreshCw className={`h-4 w-4 ${isRegenerating ? 'animate-spin' : ''}`} />
              {isRegenerating ? "Regenerating..." : "Regenerate"}
            </Button>
            
            <Button variant="outline" className="gap-2">
              <Download className="h-4 w-4" />
              Export
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {/* Scrollable crew list */}
          <div className="space-y-3 overflow-y-auto max-h-[60vh] pr-2">
            {crewRosters.map((crew) => {
              const filtered = filterAssignments(crew.assignments);
              if (filtered.length === 0) return null;
              return (
                <div
                  key={crew.crew_id}
                  className="flex items-center justify-between p-3 rounded-lg border border-border hover:shadow-md transition-shadow"
                >
                  <div className="flex items-center gap-3 min-w-0 w-full">
                    <Badge className={getCrewColor(crew.role)}>
                      {crew.role === "captain" ? "CPT" : 
                       crew.role === "first-officer" ? "FO" : "FA"}
                    </Badge>
                    <span className="font-medium whitespace-nowrap">{crew.name}</span>
                    {/* Assignment badges row with fade and +N more */}
                    <div className="relative flex-1 min-w-0 overflow-x-hidden" style={{ maxWidth: '100%' }}>
                      <div className="flex gap-1 flex-nowrap pr-8 whitespace-nowrap">
                        {filtered.slice(0, MAX_BADGES).map((a, idx) => (
                          <Badge key={a.id} variant="outline" className="ml-1">
                            {a.flight} <span className="ml-1 text-xs text-muted-foreground">{a.duty_start ? format(a.duty_start, 'MMM d') : ''}</span>
                          </Badge>
                        ))}
                        {filtered.length > MAX_BADGES && (
                          <Badge variant="secondary" className="ml-1">+{filtered.length - MAX_BADGES} more</Badge>
                        )}
                      </div>
                      {/* Fading effect on the right, adaptive to theme */}
                      <div className="pointer-events-none absolute top-0 right-0 h-full w-12 fade-right" />
                    </div>
                  </div>
                  {/* Show status of the latest assignment in the period */}
                  <Badge className={getStatusColor(filtered[filtered.length-1].status)}>
                    {filtered[filtered.length-1].status}
                  </Badge>
                </div>
              );
            })}
          </div>
          {/* Summary/footer remains below the scroll area */}
          <div className="flex items-center gap-4 pt-4 border-t border-border text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4" />
              <span>{crewRosters.filter(c => filterAssignments(c.assignments).length > 0).length} crew members scheduled</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-success"></div>
              <span>{crewRosters.reduce((acc, c) => acc + filterAssignments(c.assignments).filter(a => a.status === "active").length, 0)} active</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-warning"></div>
              <span>{crewRosters.reduce((acc, c) => acc + filterAssignments(c.assignments).filter(a => a.status === "standby").length, 0)} standby</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default RosterView;
