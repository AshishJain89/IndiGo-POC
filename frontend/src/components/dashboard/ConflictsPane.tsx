import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { 
  AlertCircle, 
  Clock, 
  Users,
  ExternalLink
} from "lucide-react";

interface Conflict {
  id: string;
  type: "hard" | "soft";
  severity: "low" | "medium" | "high";
  title: string;
  description: string;
  affectedCrew: string[];
  affectedFlights: string[];
  timestamp: Date;
}


import { useEffect, useState } from "react";

export function ConflictsPane() {
  const [conflicts, setConflicts] = useState<Conflict[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/conflicts/")
      .then(res => res.ok ? res.json() : Promise.reject("Failed to fetch conflicts"))
      .then(data => {
        setConflicts(data);
        setError(null);
      })
      .catch(e => setError(e.toString()))
      .finally(() => setLoading(false));
  }, []);

  const getTypeColor = (type: string) => {
    return type === "hard" 
      ? "bg-destructive text-destructive-foreground" 
      : "bg-warning text-warning-foreground";
  };

  const getSeverityIndicator = (severity: string) => {
    const colors = {
      low: "bg-yellow-500",
      medium: "bg-orange-500", 
      high: "bg-red-500"
    };
    return colors[severity as keyof typeof colors] || colors.low;
  };

  if (loading) return <div>Loading conflicts...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-destructive" />
          Roster Conflicts
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {conflicts.map((conflict) => (
            <div
              key={conflict.id}
              className="p-3 rounded-lg border border-border hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className={`w-2 h-2 rounded-full ${getSeverityIndicator(conflict.severity)}`} />
                  <h4 className="font-medium">{conflict.title}</h4>
                </div>
                <Badge className={getTypeColor(conflict.type)}>
                  {conflict.type}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground mb-3">
                {conflict.description}
              </p>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-muted-foreground" />
                  <div className="flex gap-1">
                    {conflict.affectedCrew.map((crew) => (
                      <Badge key={crew} variant="outline" className="text-xs">
                        {crew}
                      </Badge>
                    ))}
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">
                      {new Date(conflict.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                  <Button variant="ghost" size="sm" className="gap-1 text-xs">
                    Resolve
                    <ExternalLink className="h-3 w-3" />
                  </Button>
                </div>
              </div>
            </div>
          ))}
          {conflicts.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <AlertCircle className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No conflicts detected</p>
            </div>
          )}
        </div>
        <div className="mt-4 pt-4 border-t border-border">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-destructive" />
                <span className="text-muted-foreground">
                  {conflicts.filter(c => c.type === "hard").length} hard conflicts
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-warning" />
                <span className="text-muted-foreground">
                  {conflicts.filter(c => c.type === "soft").length} soft conflicts
                </span>
              </div>
            </div>
            <Button variant="outline" size="sm">
              Resolve All
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}