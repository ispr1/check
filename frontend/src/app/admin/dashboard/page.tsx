'use client';

import { motion } from 'framer-motion';
import {
    Shield, Building2, Users, Sparkles, LogOut, Home, Settings,
    BarChart3, FileText, Server, Globe
} from 'lucide-react';
import Link from 'next/link';

const stats = [
    { label: 'Total Companies', value: '156', change: '+8', icon: Building2, color: 'cyan' },
    { label: 'Active Users', value: '2,847', change: '+124', icon: Users, color: 'indigo' },
    { label: 'Verifications Today', value: '1,234', change: '+18%', icon: BarChart3, color: 'emerald' },
    { label: 'System Health', value: '99.9%', change: '+0.1%', icon: Server, color: 'emerald' },
];

const activity = [
    { type: 'company', action: 'New company registered', name: 'TechCorp India', time: '5 min ago' },
    { type: 'user', action: 'User role updated', name: 'Priya Sharma → Admin', time: '12 min ago' },
    { type: 'system', action: 'API synchronized', name: 'All healthy', time: '1 hr ago' },
];

const sidebarItems = [
    { icon: Home, label: 'Dashboard', href: '/admin/dashboard', active: true },
    { icon: Building2, label: 'Companies', href: '/admin/companies' },
    { icon: Users, label: 'Users', href: '/admin/users' },
    { icon: BarChart3, label: 'Analytics', href: '/admin/analytics' },
    { icon: Globe, label: 'API Health', href: '/admin/api-health' },
    { icon: FileText, label: 'Logs', href: '/admin/logs' },
    { icon: Settings, label: 'Settings', href: '/admin/settings' },
];

export default function AdminDashboard() {
    return (
        <div className="min-h-screen bg-[#0a0a0f] flex">
            {/* Sidebar */}
            <aside className="w-64 bg-[#0f0f15] border-r border-white/5 flex flex-col">
                <div className="p-5 border-b border-white/5">
                    <Link href="/" className="flex items-center gap-2">
                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                            <Sparkles className="w-4 h-4 text-white" />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-sm font-semibold text-white">Kovanent</span>
                            <span className="text-[9px] text-violet-400 uppercase tracking-wider -mt-0.5">Admin</span>
                        </div>
                    </Link>
                </div>

                <nav className="flex-1 p-3 space-y-1">
                    {sidebarItems.map((item) => (
                        <Link
                            key={item.label}
                            href={item.href}
                            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${item.active ? 'text-white bg-white/5' : 'text-white/40 hover:text-white hover:bg-white/5'
                                }`}
                        >
                            <item.icon className="w-4 h-4" />
                            {item.label}
                        </Link>
                    ))}
                </nav>

                <div className="p-3 border-t border-white/5">
                    <div className="flex items-center gap-3 p-3 rounded-lg bg-white/[0.02]">
                        <div className="w-9 h-9 rounded-lg bg-violet-500/20 flex items-center justify-center">
                            <Shield className="w-4 h-4 text-violet-400" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium text-white truncate">Super Admin</div>
                            <div className="text-xs text-white/40 truncate">admin@kovanent.io</div>
                        </div>
                        <button className="text-white/40 hover:text-white">
                            <LogOut className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            </aside>

            {/* Main */}
            <main className="flex-1 overflow-auto">
                <header className="sticky top-0 z-10 bg-[#0a0a0f]/90 backdrop-blur-sm border-b border-white/5 px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-xl font-semibold text-white">Admin Dashboard</h1>
                            <p className="text-sm text-white/40 mt-0.5">System overview and management</p>
                        </div>
                        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
                            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                            <span className="text-sm text-emerald-400 font-medium">All Systems Operational</span>
                        </div>
                    </div>
                </header>

                <div className="p-6">
                    {/* Stats */}
                    <div className="grid grid-cols-4 gap-4 mb-6">
                        {stats.map((stat) => (
                            <motion.div
                                key={stat.label}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className="card p-5"
                            >
                                <div className="flex items-start justify-between mb-3">
                                    <div className={`w-10 h-10 rounded-lg bg-${stat.color}-500/10 flex items-center justify-center`}>
                                        <stat.icon className={`w-5 h-5 text-${stat.color}-400`} />
                                    </div>
                                    <span className="text-xs font-medium text-emerald-400">{stat.change}</span>
                                </div>
                                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                                <div className="text-xs text-white/40">{stat.label}</div>
                            </motion.div>
                        ))}
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        {/* Activity */}
                        <div className="card p-5">
                            <h2 className="text-base font-semibold text-white mb-4">Recent Activity</h2>
                            <div className="space-y-3">
                                {activity.map((a, i) => (
                                    <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-white/[0.02]">
                                        <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${a.type === 'company' ? 'bg-cyan-500/10' : a.type === 'user' ? 'bg-indigo-500/10' : 'bg-emerald-500/10'
                                            }`}>
                                            {a.type === 'company' ? <Building2 className="w-4 h-4 text-cyan-400" /> :
                                                a.type === 'user' ? <Users className="w-4 h-4 text-indigo-400" /> :
                                                    <Server className="w-4 h-4 text-emerald-400" />}
                                        </div>
                                        <div className="flex-1 min-w-0">
                                            <div className="text-sm text-white">{a.action}</div>
                                            <div className="text-xs text-white/40">{a.name}</div>
                                        </div>
                                        <div className="text-xs text-white/30">{a.time}</div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Metrics */}
                        <div className="card p-5">
                            <h2 className="text-base font-semibold text-white mb-4">System Metrics</h2>
                            <div className="space-y-4">
                                <div>
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm text-white/60">API Response Time</span>
                                        <span className="text-sm font-medium text-emerald-400">45ms</span>
                                    </div>
                                    <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                                        <div className="h-full w-[15%] rounded-full bg-emerald-500" />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm text-white/60">Database Load</span>
                                        <span className="text-sm font-medium text-cyan-400">32%</span>
                                    </div>
                                    <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                                        <div className="h-full w-[32%] rounded-full bg-cyan-500" />
                                    </div>
                                </div>
                                <div>
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm text-white/60">Memory Usage</span>
                                        <span className="text-sm font-medium text-indigo-400">58%</span>
                                    </div>
                                    <div className="h-1.5 rounded-full bg-white/5 overflow-hidden">
                                        <div className="h-full w-[58%] rounded-full bg-indigo-500" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
