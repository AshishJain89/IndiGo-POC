import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  AlertTriangle, 
  Plus, 
  Clock, 
  Plane,
  AlertCircle
} from "lucide-react";

interface Disruption {
  id: string;
  type: "foreseen" | "unforeseen";
  severity: "low" | "medium" | "high" | "critical";
  title: string;
  description: string;
  affectedFlights: string[];
  timestamp: Date;
}

interface DisruptionForm {
  type: "foreseen" | "unforeseen";
  severity: "low" | "medium" | "high" | "critical";
  title: string;
  description: string;
  affectedFlights: string;
}

export default function DisruptionsPanel() {
  const [disruptions, setDisruptions] = useState<Disruption[]>([]);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState<DisruptionForm>({
    type: "unforeseen",
    severity: "low",
    title: "",
    description: "",
    affectedFlights: ""
  });
  const [submitting, setSubmitting] = useState(false);

  // Fetch disruptions from backend
  const fetchDisruptions = () => {
    setLoading(true);
    fetch("/api/disruptions/")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch disruptions");
        return res.json();
      })
      .then((data) => {
        setDisruptions(
          data.map((d: any) => ({
            ...d,
            timestamp: d.timestamp ? new Date(d.timestamp) : new Date(),
          }))
        );
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDisruptions();
  }, []);

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "low": return "bg-muted text-muted-foreground";
      case "medium": return "bg-warning text-warning-foreground";
      case "high": return "bg-destructive text-destructive-foreground";
      case "critical": return "bg-red-600 text-white";
      default: return "bg-muted text-muted-foreground";
    }
  };

  const getTypeIcon = (type: string) => {
    return type === "foreseen" ? (
      <Clock className="h-4 w-4" />
    ) : (
      <AlertCircle className="h-4 w-4" />
    );
  };

  const handleFormChange = (field: keyof DisruptionForm, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleAddDisruption = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      const res = await fetch("/api/disruptions/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: form.type,
          severity: form.severity,
          title: form.title,
          description: form.description,
          affectedFlights: form.affectedFlights.split(",").map(f => f.trim()).filter(Boolean)
        })
      });
      if (!res.ok) throw new Error("Failed to add disruption");
      setIsDialogOpen(false);
      setForm({ type: "unforeseen", severity: "low", title: "", description: "", affectedFlights: "" });
      fetchDisruptions();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 mb-2">
          <AlertTriangle className="h-5 w-5 text-warning" />
          Disruptions
        </CardTitle>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button size="sm" className="gap-2">
              <Plus className="h-4 w-4" />
              Add Disruption
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>Add Manual Disruption</DialogTitle>
            </DialogHeader>
            <form className="space-y-4" onSubmit={handleAddDisruption}>
              <div>
                <Label htmlFor="title">Title</Label>
                <Input id="title" value={form.title} onChange={e => handleFormChange("title", e.target.value)} placeholder="Disruption title..." required />
              </div>
              <div>
                <Label htmlFor="type">Type</Label>
                <Select value={form.type} onValueChange={val => handleFormChange("type", val as any)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="foreseen">Foreseen</SelectItem>
                    <SelectItem value="unforeseen">Unforeseen</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="severity">Severity</Label>
                <Select value={form.severity} onValueChange={val => handleFormChange("severity", val as any)}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select severity" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="low">Low</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="critical">Critical</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea id="description" value={form.description} onChange={e => handleFormChange("description", e.target.value)} placeholder="Describe the disruption..." required />
              </div>
              <div>
                <Label htmlFor="flights">Affected Flights</Label>
                <Input id="flights" value={form.affectedFlights} onChange={e => handleFormChange("affectedFlights", e.target.value)} placeholder="e.g., UA1234, UA5678" />
              </div>
              <Button className="w-full" type="submit" disabled={submitting}>{submitting ? "Adding..." : "Add Disruption"}</Button>
            </form>
          </DialogContent>
        </Dialog>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {disruptions.map((disruption) => (
            <div
              key={disruption.id}
              className="p-3 rounded-lg border border-border hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  {getTypeIcon(disruption.type)}
                  <h4 className="font-medium">{disruption.title}</h4>
                </div>
                <Badge className={getSeverityColor(disruption.severity)}>
                  {disruption.severity}
                </Badge>
              </div>
              <p className="text-sm text-muted-foreground mb-3">
                {disruption.description}
              </p>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Plane className="h-4 w-4 text-muted-foreground" />
                  <div className="flex gap-1">
                    {disruption.affectedFlights.map((flight) => (
                      <Badge key={flight} variant="outline" className="text-xs">
                        {flight}
                      </Badge>
                    ))}
                  </div>
                </div>
                <span className="text-xs text-muted-foreground">
                  {disruption.timestamp.toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
          {disruptions.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <AlertTriangle className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p>No disruptions reported</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}