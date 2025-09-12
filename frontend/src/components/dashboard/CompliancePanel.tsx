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
  Shield, 
  Edit, 
  RefreshCw, 
  AlertTriangle,
  CheckCircle,
  XCircle
} from "lucide-react";

interface ComplianceRule {
  id: string;
  name: string;
  type: "hard" | "soft";
  description: string;
  status: "active" | "inactive";
  violations: number;
}


export function CompliancePanel() {
  const [rules, setRules] = useState<ComplianceRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/compliance/rules")
      .then(res => res.ok ? res.json() : Promise.reject("Failed to fetch rules"))
      .then(data => {
        setRules(data);
        setError(null);
      })
      .catch(e => setError(e.toString()))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading compliance rules...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);

  const fetchRules = () => {
    setLoading(true);
    fetch("/api/compliance/rules")
      .then(res => res.ok ? res.json() : Promise.reject("Failed to fetch rules"))
      .then(data => {
        setRules(data);
        setError(null);
      })
      .catch(e => setError(e.toString()))
      .finally(() => setLoading(false));
  };

  const handleUpdateRules = async () => {
    setIsUpdating(true);
    setError(null);
    try {
      const res = await fetch("/api/compliance/rules/update", {
        method: "POST",
      });
      if (!res.ok) throw new Error("Failed to update rules");
      fetchRules();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsUpdating(false);
    }
  };

  const getTypeColor = (type: string) => {
    return type === "hard" 
      ? "bg-destructive text-destructive-foreground" 
      : "bg-warning text-warning-foreground";
  };

  const getStatusIcon = (violations: number, type: string) => {
    if (violations === 0) {
      return <CheckCircle className="h-4 w-4 text-success" />;
    } else if (type === "hard" && violations > 0) {
      return <XCircle className="h-4 w-4 text-destructive" />;
    } else {
      return <AlertTriangle className="h-4 w-4 text-warning" />;
    }
  };

  return (
    <Card className="shadow-lg w-full max-w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 min-w-0 mb-2">
          <Shield className="h-5 w-5 text-primary flex-shrink-0" />
          <span className="truncate whitespace-nowrap">Compliance Policy</span>
        </CardTitle>
        <div className="flex gap-2 flex-shrink-0">
          <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" size="sm" className="gap-2">
                <Edit className="h-4 w-4" />
                Edit Policy
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>Edit Compliance Rule</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="rule-name">Rule Name</Label>
                  <Input id="rule-name" placeholder="Rule name..." />
                </div>
                <div>
                  <Label htmlFor="rule-type">Type</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="hard">Hard Rule</SelectItem>
                      <SelectItem value="soft">Soft Rule</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="rule-description">Description</Label>
                  <Textarea id="rule-description" placeholder="Rule description..." />
                </div>
                <Button className="w-full">Save Rule</Button>
              </div>
            </DialogContent>
          </Dialog>
          <Button 
            onClick={handleUpdateRules}
            disabled={isUpdating}
            size="sm" 
            className="gap-2"
          >
            <RefreshCw className={`h-4 w-4 ${isUpdating ? 'animate-spin' : ''}`} />
            {isUpdating ? "Updating..." : "Check Updates"}
          </Button>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-3">
          {rules.map((rule) => (
            <div
              key={rule.id}
              className="p-3 rounded-lg border border-border hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-2 min-w-0">
                <div className="flex items-center gap-2 min-w-0">
                  {getStatusIcon(rule.violations, rule.type)}
                  <h4 className="font-medium truncate whitespace-nowrap min-w-0 max-w-xs">{rule.name}</h4>
                </div>
                <div className="flex items-center gap-2 flex-shrink-0">
                  <Badge className={getTypeColor(rule.type) + ' truncate whitespace-nowrap'}>
                    {rule.type}
                  </Badge>
                  {rule.violations > 0 && (
                    <Badge variant="outline" className="text-destructive border-destructive truncate whitespace-nowrap">
                      {rule.violations} violations
                    </Badge>
                  )}
                </div>
              </div>
              <p className="text-sm text-muted-foreground truncate max-w-full">
                {rule.description}
              </p>
            </div>
          ))}
        </div>
        
        <div className="mt-4 pt-4 border-t border-border">
          <div className="flex items-center justify-between text-sm min-w-0 flex-wrap">
            <div className="flex items-center gap-4 min-w-0 flex-wrap">
              <div className="flex items-center gap-2 min-w-0">
                <CheckCircle className="h-4 w-4 text-success flex-shrink-0" />
                <span className="text-muted-foreground truncate whitespace-nowrap">
                  {rules.filter(r => r.violations === 0).length} compliant
                </span>
              </div>
              <div className="flex items-center gap-2 min-w-0">
                <AlertTriangle className="h-4 w-4 text-warning flex-shrink-0" />
                <span className="text-muted-foreground truncate whitespace-nowrap">
                  {rules.filter(r => r.violations > 0).length} with violations
                </span>
              </div>
            </div>
            <span className="text-muted-foreground truncate whitespace-nowrap">
              Total violations: {rules.reduce((sum, rule) => sum + rule.violations, 0)}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
