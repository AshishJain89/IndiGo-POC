import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { 
  Users, 
  Search, 
  Filter,
  Clock,
  Calendar,
  Star
} from "lucide-react";

interface CrewMember {
  id: string;
  name: string;
  role: "captain" | "first-officer" | "flight-attendant";
  status: "active" | "standby" | "rest" | "vacation";
  rating: number;
  hoursThisMonth: number;
  nextDuty: Date;
  homeBase: string;
  qualifications: string[];
}




export function CrewView() {
  const [selectedCrew, setSelectedCrew] = useState<CrewMember | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [crewMembers, setCrewMembers] = useState<CrewMember[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/crew/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch crew");
        return res.json();
      })
      .then((data) => {
        setCrewMembers(
          data.map((c: any) => ({
            ...c,
            name: c.first_name + ' ' + c.last_name,
            role: c.rank?.toLowerCase().replace('_', '-') || '',
            status: c.status?.toLowerCase() || '',
            rating: c.performance_rating || 0,
            hoursThisMonth: c.total_flight_hours_month || 0,
            nextDuty: c.duty_start_time ? new Date(c.duty_start_time) : new Date(),
            homeBase: c.base_airport || '',
            qualifications: c.qualifications || [],
          }))
        );
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredCrew = crewMembers.filter(crew =>
    crew.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    crew.role.toLowerCase().includes(searchTerm.toLowerCase()) ||
    crew.homeBase.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
      case "vacation": return "bg-accent text-accent-foreground";
      default: return "bg-muted text-muted-foreground";
    }
  };

  const getRoleDisplayName = (role: string) => {
    switch (role) {
      case "captain": return "Captain";
      case "first-officer": return "First Officer";
      case "flight-attendant": return "Flight Attendant";
      default: return role;
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Users className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">Crew Management</h1>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search crew members..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-64"
            />
          </div>
          <Button variant="outline" className="gap-2">
            <Filter className="h-4 w-4" />
            Filter
          </Button>
        </div>
      </div>

  <div className="flex flex-col gap-2">
        {filteredCrew.map((crew) => (
          <Card 
            key={crew.id} 
            className="cursor-pointer hover:shadow-md transition-shadow px-2 py-1 min-h-0"
            onClick={() => setSelectedCrew(crew)}
          >
            <CardHeader className="pb-1 px-0 py-0 min-h-0">
              <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1 min-h-0 w-full text-[15px]">
                <div className="flex flex-wrap items-center gap-x-2 gap-y-1 min-w-0">
                  <CardTitle className="text-[15px] leading-tight font-semibold whitespace-nowrap mb-0">{crew.name}</CardTitle>
                  <Badge className={getCrewColor(crew.role) + ' text-[11px] px-2 py-0.5'}>
                    {crew.role === "captain" ? "CPT" : crew.role === "first-officer" ? "FO" : "FA"}
                  </Badge>
                  <Badge className={getStatusColor(crew.status) + ' text-[11px] px-2 py-0.5'}>
                    {crew.status}
                  </Badge>
                  <span className="text-muted-foreground text-[13px] leading-tight whitespace-nowrap ml-1">{getRoleDisplayName(crew.role)}</span>
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 ml-3 min-w-0">
                    <div className="flex items-center gap-1 min-w-0">
                      <span className="text-muted-foreground text-[13px]">Hours:</span>
                      <span className="font-semibold text-[13px]">{crew.hoursThisMonth}h</span>
                    </div>
                    <div className="flex items-center gap-1 min-w-0">
                      <span className="text-muted-foreground text-[13px]">Base:</span>
                      <Badge variant="outline" className="text-[11px] px-2 py-0.5">{crew.homeBase}</Badge>
                    </div>
                    <div className="flex items-center gap-1 min-w-0">
                      <span className="text-muted-foreground text-[13px]">Next:</span>
                      <span className="font-semibold text-[12px]">
                        {crew.nextDuty.toLocaleDateString()} {crew.nextDuty.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-1 ml-auto">
                  <Star className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                  <span className="text-[13px] font-semibold">{crew.rating}</span>
                </div>
              </div>
            </CardHeader>
            <CardContent className="hidden" />
          </Card>
        ))}
      </div>

      {/* Crew Detail Modal */}
      <Dialog open={!!selectedCrew} onOpenChange={() => setSelectedCrew(null)}>
        <DialogContent className="max-w-2xl">
          {selectedCrew && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-3">
                  <Badge className={getCrewColor(selectedCrew.role)}>
                    {selectedCrew.role === "captain" ? "CPT" : 
                     selectedCrew.role === "first-officer" ? "FO" : "FA"}
                  </Badge>
                  {selectedCrew.name}
                  <Badge className={getStatusColor(selectedCrew.status)}>
                    {selectedCrew.status}
                  </Badge>
                </DialogTitle>
              </DialogHeader>
              
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold mb-2 flex items-center gap-2">
                      <Clock className="h-4 w-4" />
                      Schedule Details
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Hours this month:</span>
                        <span>{selectedCrew.hoursThisMonth}h</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Home base:</span>
                        <span>{selectedCrew.homeBase}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Rating:</span>
                        <div className="flex items-center gap-1">
                          <Star className="h-3 w-3 text-yellow-500 fill-yellow-500" />
                          <span>{selectedCrew.rating}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Qualifications</h3>
                    <div className="flex flex-wrap gap-1">
                      {selectedCrew.qualifications.map((qual) => (
                        <Badge key={qual} variant="secondary" className="text-xs">
                          {qual}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Upcoming Schedule (7 days)
                  </h3>
                  <div className="space-y-2">
                    {/* Mock schedule data */}
                    <div className="flex items-center justify-between p-2 rounded border">
                      <div>
                        <span className="font-medium">UA1234 LAX → JFK</span>
                        <p className="text-sm text-muted-foreground">Jan 15, 08:00 - 16:30</p>
                      </div>
                      <Badge variant="outline">Active</Badge>
                    </div>
                    <div className="flex items-center justify-between p-2 rounded border">
                      <div>
                        <span className="font-medium">Rest Period</span>
                        <p className="text-sm text-muted-foreground">Jan 16, 00:00 - 23:59</p>
                      </div>
                      <Badge className="bg-muted text-muted-foreground">Rest</Badge>
                    </div>
                    <div className="flex items-center justify-between p-2 rounded border">
                      <div>
                        <span className="font-medium">UA5678 JFK → LAX</span>
                        <p className="text-sm text-muted-foreground">Jan 17, 10:00 - 18:30</p>
                      </div>
                      <Badge className="bg-warning text-warning-foreground">Standby</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
