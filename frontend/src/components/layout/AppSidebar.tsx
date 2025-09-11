import { useState } from "react";
import { 
  Calendar, 
  Users, 
  Plane, 
  BarChart3,
  Home,
  MessageSquare
} from "lucide-react";
import { useLocation } from "react-router-dom";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
  useSidebar,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";

const navigationItems = [
  { id: "dashboard", label: "Dashboard", icon: Home },
  { id: "crew", label: "Crew", icon: Users },
  { id: "flights", label: "Flights", icon: Plane },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
];

interface AppSidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  onChatToggle: () => void;
}

export function AppSidebar({ activeView, onViewChange, onChatToggle }: AppSidebarProps) {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";

  const isActive = (id: string) => activeView === id;
  const isExpanded = navigationItems.some((item) => isActive(item.id));

  return (
    <Sidebar className="border-r border-border shadow-sm pt-16 w-64 min-w-[16rem] max-w-[16rem] flex-shrink-0">
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="whitespace-nowrap truncate">Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    onClick={() => onViewChange(item.id)}
                    isActive={isActive(item.id)}
                    className="w-full"
                  >
                    <item.icon className="h-4 w-4 flex-shrink-0" />
                    {!collapsed && <span className="ml-2 truncate whitespace-nowrap">{item.label}</span>}
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={onChatToggle} className="w-full">
              <MessageSquare className="h-4 w-4 flex-shrink-0" />
              {!collapsed && <span className="ml-2 truncate whitespace-nowrap">AI Assistant</span>}
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}