'use client';

import { motion } from 'framer-motion';
import {
    Users, FileCheck, Clock, CheckCircle2, AlertTriangle,
    Search, ChevronRight, Sparkles, LogOut, Home, Settings, BarChart3, FileText
} from 'lucide-react';
import Link from 'next/link';

const stats = [
    { label: 'Total Verifications', value: '1,234', change: '+12%', icon: FileCheck, color: 'indigo' },
    { label: 'Pending Review', value: '23', change: '-5', icon: Clock, color: 'amber' },
    { label: 'Verified Today', value: '47', change: '+8', icon: CheckCircle2, color: 'emerald' },
    { label: 'Flagged', value: '3', change: '+1', icon: AlertTriangle, color: 'red' },
];

const verifications = [
    { id: 1, name: 'Priya Sharma', email: 'priya.s@techcorp.com', score: 94, status: 'VERIFIED', time: '2 min ago' },
    { id: 2, name: 'Rahul Verma', email: 'rahul.v@startup.io', score: 72, status: 'REVIEW', time: '15 min ago' },
    { id: 3, name: 'Ananya Patel', email: 'ananya@enterprise.com', score: 88, status: 'VERIFIED', time: '1 hr ago' },
    { id: 4, name: 'Vikram Singh', email: 'vikram@corp.in', score: 45, status: 'FLAGGED', time: '2 hr ago' },
];

const sidebarItems = [
    { icon: Home, label: 'Dashboard', href: '/hr/dashboard', active: true },
    { icon: FileCheck, label: 'Verifications', href: '/hr/verifications' },
    { icon: Users, label: 'Candidates', href: '/hr/candidates' },
    { icon: BarChart3, label: 'Analytics', href: '/hr/analytics' },
    { icon: FileText, label: 'Reports', href: '/hr/reports' },
    { icon: Settings, label: 'Settings', href: '/hr/settings' },
];

export default function HRDashboard() {
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
                            <span className="text-[9px] text-indigo-400 uppercase tracking-wider -mt-0.5">HR Portal</span>
                        </div>
                    </Link>
                </div>

                <nav className="flex-1 p-3 space-y-1">
                    {sidebarItems.map((item) => (
                        <Link
                            key={item.label}
                            href={item.href}
                            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${item.active
                                    ? 'text-white bg-white/5'
                                    : 'text-white/40 hover:text-white hover:bg-white/5'
                                }`}
                        >
                            <item.icon className="w-4 h-4" />
                            {item.label}
                        </Link>
                    ))}
                </nav>

                <div className="p-3 border-t border-white/5">
                    <div className="flex items-center gap-3 p-3 rounded-lg bg-white/[0.02]">
                        <div className="w-9 h-9 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-semibold text-sm">
                            HR
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium text-white truncate">HR Manager</div>
                            <div className="text-xs text-white/40 truncate">hr@company.com</div>
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
                            <h1 className="text-xl font-semibold text-white">Dashboard</h1>
                            <p className="text-sm text-white/40 mt-0.5">Welcome back, HR Manager</p>
                        </div>
                        <div className="relative">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/30" />
                            <input
                                type="text"
                                placeholder="Search candidates..."
                                className="w-56 pl-9 pr-4 py-2 rounded-lg bg-white/5 border border-white/10 text-sm text-white placeholder:text-white/30 focus:outline-none focus:border-indigo-500/50"
                            />
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
                                    <span className={`text-xs font-medium ${stat.change.startsWith('+') ? 'text-emerald-400' : 'text-red-400'}`}>
                                        {stat.change}
                                    </span>
                                </div>
                                <div className="text-2xl font-bold text-white mb-1">{stat.value}</div>
                                <div className="text-xs text-white/40">{stat.label}</div>
                            </motion.div>
                        ))}
                    </div>

                    {/* Table */}
                    <div className="card p-5">
                        <div className="flex items-center justify-between mb-5">
                            <h2 className="text-base font-semibold text-white">Recent Verifications</h2>
                            <Link href="/hr/verifications" className="flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300">
                                View all <ChevronRight className="w-4 h-4" />
                            </Link>
                        </div>

                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-white/5">
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Candidate</th>
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Trust Score</th>
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Status</th>
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Time</th>
                                    <th className="text-right text-xs font-medium text-white/40 uppercase pb-3">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {verifications.map((v) => (
                                    <tr key={v.id} className="group hover:bg-white/[0.02]">
                                        <td className="py-3">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center text-xs text-white font-medium">
                                                    {v.name.split(' ').map(n => n[0]).join('')}
                                                </div>
                                                <div>
                                                    <div className="text-sm font-medium text-white">{v.name}</div>
                                                    <div className="text-xs text-white/40">{v.email}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="py-3">
                                            <div className="flex items-center gap-2">
                                                <div className="w-10 h-1.5 rounded-full bg-white/10 overflow-hidden">
                                                    <div
                                                        className={`h-full rounded-full ${v.score >= 85 ? 'bg-emerald-500' : v.score >= 70 ? 'bg-amber-500' : 'bg-red-500'}`}
                                                        style={{ width: `${v.score}%` }}
                                                    />
                                                </div>
                                                <span className={`text-sm font-semibold ${v.score >= 85 ? 'text-emerald-400' : v.score >= 70 ? 'text-amber-400' : 'text-red-400'}`}>
                                                    {v.score}
                                                </span>
                                            </div>
                                        </td>
                                        <td className="py-3">
                                            <span className={`inline-flex px-2 py-1 rounded text-xs font-medium ${v.status === 'VERIFIED' ? 'text-emerald-400 bg-emerald-500/10' :
                                                    v.status === 'REVIEW' ? 'text-amber-400 bg-amber-500/10' :
                                                        'text-red-400 bg-red-500/10'
                                                }`}>
                                                {v.status}
                                            </span>
                                        </td>
                                        <td className="py-3 text-sm text-white/40">{v.time}</td>
                                        <td className="py-3 text-right">
                                            <button className="text-sm text-indigo-400 hover:text-indigo-300 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                                                Review
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
        </div>
    );
}
