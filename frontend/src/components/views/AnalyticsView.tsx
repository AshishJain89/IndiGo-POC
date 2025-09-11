import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Users,
  Clock,
  Shield,
  Activity,
  FileText,
  AlertTriangle,
  CheckCircle
} from "lucide-react";

interface MetricCard {
  title: string;
  value: string;
  change: string;
  trend: "up" | "down" | "stable";
  icon: React.ReactNode;
};

interface ViolationItem {
  id: string;
  rule: string;
  description: string;
  severity: "low" | "medium" | "high";
  crew: string;
  timestamp: Date;
};

interface AuditLogEntry {
  id: string;
  timestamp: Date;
  user: string;
  action: string;
  details: string;
  type: "roster_change" | "rule_update" | "disruption" | "system";
};


// ...existing type definitions...


export const AnalyticsView = () => {
  const [metrics, setMetrics] = useState<MetricCard[]>([]);
  const [violations, setViolations] = useState<ViolationItem[]>([]);
  const [auditLog, setAuditLog] = useState<AuditLogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeFilter, setTimeFilter] = useState<"daily" | "weekly" | "monthly">("weekly");
  const [isAuditOpen, setIsAuditOpen] = useState(false);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch("/api/analytics/metrics").then(r => r.ok ? r.json() : Promise.reject("metrics")),
      fetch("/api/analytics/violations").then(r => r.ok ? r.json() : Promise.reject("violations")),
      fetch("/api/analytics/auditlog").then(r => r.ok ? r.json() : Promise.reject("auditlog")),
    ])
      .then(([metricsData, violationsData, auditLogData]) => {
        setMetrics(metricsData);
        setViolations(violationsData);
        setAuditLog(auditLogData);
        setError(null);
      })
      .catch(e => setError(`Failed to fetch analytics data: ${e}`))
      .finally(() => setLoading(false));
  }, []);

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up": return <TrendingUp className="h-4 w-4 text-success" />;
      case "down": return <TrendingDown className="h-4 w-4 text-destructive" />;
      default: return <div className="h-4 w-4" />;
    }
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "up": return "text-success";
      case "down": return "text-destructive";
      default: return "text-muted-foreground";
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "low": return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "medium": return "bg-orange-100 text-orange-800 border-orange-200";
      case "high": return "bg-red-100 text-red-800 border-red-200";
      default: return "bg-muted text-muted-foreground";
    }
  };

  const getActionTypeColor = (type: string) => {
    switch (type) {
      case "roster_change": return "bg-primary/10 text-primary";
      case "rule_update": return "bg-warning/10 text-warning";
      case "disruption": return "bg-destructive/10 text-destructive";
      case "system": return "bg-muted text-muted-foreground";
      default: return "bg-muted text-muted-foreground";
    }
  };

  if (loading) return <div>Loading analytics...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BarChart3 className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex rounded-lg border border-border p-1">
            <Button
              variant={timeFilter === "daily" ? "default" : "ghost"}
              size="sm"
              onClick={() => setTimeFilter("daily")}
            >
              Daily
            </Button>
            <Button
              variant={timeFilter === "weekly" ? "default" : "ghost"}
              size="sm"
              onClick={() => setTimeFilter("weekly")}
            >
              Weekly
            </Button>
            <Button
              variant={timeFilter === "monthly" ? "default" : "ghost"}
              size="sm"
              onClick={() => setTimeFilter("monthly")}
            >
              Monthly
            </Button>
          </div>
          <Dialog open={isAuditOpen} onOpenChange={setIsAuditOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" className="gap-2">
                <FileText className="h-4 w-4" />
                Audit Logs
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader>
                <DialogTitle>System Audit Logs</DialogTitle>
              </DialogHeader>
              <ScrollArea className="max-h-96">
                <div className="space-y-2">
                  {auditLog.map((entry) => (
                    <div key={entry.id} className="p-3 rounded border border-border">
                      <div className="flex items-start justify-between mb-1">
                        <div className="flex items-center gap-2">
                          <Badge className={getActionTypeColor(entry.type)}>
                            {entry.action}
                          </Badge>
                          <span className="text-sm font-medium">{entry.user}</span>
                        </div>
                        <span className="text-xs text-muted-foreground">
                          {new Date(entry.timestamp).toLocaleString()}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground">{entry.details}</p>
                    </div>
                  ))}
                </div>
              </ScrollArea>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">{metric.title}</p>
                  <p className="text-2xl font-bold">{metric.value}</p>
                  <div className={`flex items-center gap-1 text-sm ${getTrendColor(metric.trend)}`}>
                    {getTrendIcon(metric.trend)}
                    <span>{metric.change} from last {timeFilter.slice(0, -2)}</span>
                  </div>
                </div>
                <div className="text-primary">
                  {metric.icon}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Violations Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-warning" />
              Soft Rule Violations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {violations.map((violation) => (
                <div key={violation.id} className="p-3 rounded border border-border">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-medium text-sm">{violation.rule}</h4>
                    <Badge className={getSeverityColor(violation.severity)}>
                      {violation.severity}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-1">
                    {violation.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <Badge variant="outline" className="text-xs">
                      {violation.crew}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {new Date(violation.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Performance Insights */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-primary" />
              Performance Insights
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="p-3 rounded border border-border">
                <h4 className="font-medium mb-2">Peak Performance Hours</h4>
                <p className="text-sm text-muted-foreground">
                  Crew performs best during 8AM-2PM shifts with 15% higher efficiency
                </p>
              </div>
              <div className="p-3 rounded border border-border">
                <h4 className="font-medium mb-2">Optimal Rest Periods</h4>
                <p className="text-sm text-muted-foreground">
                  12-hour rest periods show 23% better crew satisfaction vs 8-hour minimum
                </p>
              </div>
              <div className="p-3 rounded border border-border">
                <h4 className="font-medium mb-2">Route Preferences</h4>
                <p className="text-sm text-muted-foreground">
                  Domestic routes have 18% higher crew satisfaction than international
                </p>
              </div>
              <div className="p-3 rounded border border-border">
                <h4 className="font-medium mb-2">Disruption Patterns</h4>
                <p className="text-sm text-muted-foreground">
                  Weather-related disruptions peak at 3PM-6PM on weekdays
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};