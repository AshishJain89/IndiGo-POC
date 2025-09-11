import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { 
  Plane, 
  Search, 
  Filter,
  Clock,
  Users,
  MapPin,
  AlertTriangle
} from "lucide-react";

interface Flight {
  id: string;
  flightNumber: string;
  aircraft: string;
  route: {
    from: string;
    to: string;
  };
  departure: Date;
  arrival: Date;
  status: "on-time" | "delayed" | "cancelled" | "boarding";
  assignedCrew: {
    captain?: string;
    firstOfficer?: string;
    flightAttendants: string[];
  };
  requiredQualifications: string[];
  conflicts: string[];
}




export function FlightView() {
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [flights, setFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/flights/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch flights");
        return res.json();
      })
      .then((data) => {
        // Convert string dates to Date objects
        setFlights(
          data.map((f: any) => ({
            ...f,
            departure: new Date(f.departure),
            arrival: new Date(f.arrival),
          }))
        );
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredFlights = flights.filter(flight =>
    flight.flightNumber.toLowerCase().includes(searchTerm.toLowerCase()) ||
    flight.route.from.toLowerCase().includes(searchTerm.toLowerCase()) ||
    flight.route.to.toLowerCase().includes(searchTerm.toLowerCase()) ||
    flight.aircraft.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case "on-time": return "bg-success text-success-foreground";
      case "delayed": return "bg-warning text-warning-foreground";
      case "cancelled": return "bg-destructive text-destructive-foreground";
      case "boarding": return "bg-accent text-accent-foreground";
      default: return "bg-muted text-muted-foreground";
    }
  };

  const getCrewCount = (crew: Flight['assignedCrew']) => {
    let count = 0;
    if (crew.captain) count++;
    if (crew.firstOfficer) count++;
    count += crew.flightAttendants.length;
    return count;
  };

  const getRequiredCrewCount = () => {
    return 4; // Typically: 1 Captain + 1 FO + 2 FAs
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Plane className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">Flight Management</h1>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search flights..."
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
        {filteredFlights.map((flight) => (
          <Card 
            key={flight.id} 
            className="cursor-pointer hover:shadow-md transition-shadow px-2 py-1 min-h-0"
            onClick={() => setSelectedFlight(flight)}
          >
            <CardHeader className="pb-1 px-0 py-0 min-h-0">
              <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1 min-h-0 w-full text-[15px]">
                <div className="flex flex-wrap items-center gap-x-2 gap-y-1 min-w-0">
                  <CardTitle className="text-[15px] leading-tight font-semibold whitespace-nowrap mb-0">{flight.flightNumber}</CardTitle>
                  <Badge variant="outline" className="text-[11px] px-2 py-0.5">{flight.aircraft}</Badge>
                  <Badge className={getStatusColor(flight.status) + ' text-[11px] px-2 py-0.5'}>
                    {flight.status}
                  </Badge>
                  <span className="text-muted-foreground text-[13px] leading-tight whitespace-nowrap ml-1 flex items-center gap-1">
                    <MapPin className="h-3 w-3" />
                    {flight.route.from} → {flight.route.to}
                  </span>
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 ml-3 min-w-0">
                    <div className="flex items-center gap-1 min-w-0">
                      <Clock className="h-3 w-3 text-muted-foreground" />
                      <span className="text-muted-foreground text-[13px]">Dep:</span>
                      <span className="font-semibold text-[13px]">{flight.departure.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                    </div>
                    <div className="flex items-center gap-1 min-w-0">
                      <span className="text-muted-foreground text-[13px]">Arr:</span>
                      <span className="font-semibold text-[13px]">{flight.arrival.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
                    </div>
                    <div className="flex items-center gap-1 min-w-0">
                      <Users className="h-4 w-4 text-muted-foreground" />
                      <span className="text-[13px]">
                        {getCrewCount(flight.assignedCrew)}/{getRequiredCrewCount()} crew
                      </span>
                    </div>
                    {flight.conflicts.length > 0 && (
                      <div className="flex items-center gap-1 min-w-0">
                        <AlertTriangle className="h-4 w-4 text-destructive" />
                        <Badge variant="outline" className="text-destructive border-destructive text-xs">
                          {flight.conflicts.length} issues
                        </Badge>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="hidden" />
          </Card>
        ))}
      </div>

      {/* Flight Detail Modal */}
      <Dialog open={!!selectedFlight} onOpenChange={() => setSelectedFlight(null)}>
        <DialogContent className="max-w-3xl">
          {selectedFlight && (
            <>
              <DialogHeader>
                <DialogTitle className="flex items-center gap-3">
                  <Plane className="h-5 w-5" />
                  {selectedFlight.flightNumber}
                  <Badge variant="outline">{selectedFlight.aircraft}</Badge>
                  <Badge className={getStatusColor(selectedFlight.status)}>
                    {selectedFlight.status}
                  </Badge>
                </DialogTitle>
              </DialogHeader>
              
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold mb-2 flex items-center gap-2">
                      <MapPin className="h-4 w-4" />
                      Flight Details
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Route:</span>
                        <span>{selectedFlight.route.from} → {selectedFlight.route.to}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Aircraft:</span>
                        <span>{selectedFlight.aircraft}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Departure:</span>
                        <span>
                          {selectedFlight.departure.toLocaleString()}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Arrival:</span>
                        <span>
                          {selectedFlight.arrival.toLocaleString()}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h3 className="font-semibold mb-2">Required Qualifications</h3>
                    <div className="flex flex-wrap gap-1">
                      {selectedFlight.requiredQualifications.map((qual) => (
                        <Badge key={qual} variant="secondary" className="text-xs">
                          {qual}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
                
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <Users className="h-4 w-4" />
                    Assigned Crew
                  </h3>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between p-3 rounded border">
                      <div>
                        <span className="font-medium">Captain</span>
                        <p className="text-sm text-muted-foreground">
                          {selectedFlight.assignedCrew.captain || "Not assigned"}
                        </p>
                      </div>
                      <Badge className="bg-crew-captain text-white">CPT</Badge>
                    </div>
                    <div className="flex items-center justify-between p-3 rounded border">
                      <div>
                        <span className="font-medium">First Officer</span>
                        <p className="text-sm text-muted-foreground">
                          {selectedFlight.assignedCrew.firstOfficer || "Not assigned"}
                        </p>
                      </div>
                      <Badge className="bg-crew-first-officer text-white">FO</Badge>
                    </div>
                    <div className="p-3 rounded border">
                      <div className="mb-2">
                        <span className="font-medium">Flight Attendants</span>
                      </div>
                      {selectedFlight.assignedCrew.flightAttendants.length > 0 ? (
                        <div className="space-y-2">
                          {selectedFlight.assignedCrew.flightAttendants.map((fa, index) => (
                            <div key={index} className="flex items-center justify-between">
                              <span className="text-sm">{fa}</span>
                              <Badge className="bg-crew-flight-attendant text-white">FA</Badge>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-sm text-muted-foreground">No flight attendants assigned</p>
                      )}
                    </div>
                  </div>
                </div>
                
                {selectedFlight.conflicts.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-3 flex items-center gap-2 text-destructive">
                      <AlertTriangle className="h-4 w-4" />
                      Conflicts & Issues
                    </h3>
                    <div className="space-y-2">
                      {selectedFlight.conflicts.map((conflict, index) => (
                        <div key={index} className="p-2 rounded border border-destructive/20 bg-destructive/5">
                          <p className="text-sm text-destructive">{conflict}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}