'use client';

import { motion } from 'framer-motion';
import {
    Building2, Users, Sparkles, LogOut, Home, Settings,
    BarChart3, FileText, FileCheck, TrendingUp, Clock
} from 'lucide-react';
import Link from 'next/link';

const stats = [
    { label: 'Total Verifications', value: '4,567', change: '+234', icon: FileCheck, color: 'indigo' },
    { label: 'Active HR Users', value: '24', change: '+3', icon: Users, color: 'cyan' },
    { label: 'This Month', value: '892', change: '+12%', icon: TrendingUp, color: 'emerald' },
    { label: 'Avg TAT', value: '18min', change: '-2min', icon: Clock, color: 'amber' },
];

const hrUsers = [
    { id: 1, name: 'Priya Sharma', email: 'priya@company.com', role: 'Senior HR', verifications: 234, status: 'active' },
    { id: 2, name: 'Rahul Verma', email: 'rahul@company.com', role: 'HR Manager', verifications: 189, status: 'active' },
    { id: 3, name: 'Ananya Patel', email: 'ananya@company.com', role: 'HR Executive', verifications: 156, status: 'active' },
];

const sidebarItems = [
    { icon: Home, label: 'Dashboard', href: '/company/dashboard', active: true },
    { icon: Users, label: 'HR Users', href: '/company/users' },
    { icon: FileCheck, label: 'Verifications', href: '/company/verifications' },
    { icon: BarChart3, label: 'Analytics', href: '/company/analytics' },
    { icon: FileText, label: 'Reports', href: '/company/reports' },
    { icon: Settings, label: 'Settings', href: '/company/settings' },
];

export default function CompanyDashboard() {
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
                            <span className="text-[9px] text-cyan-400 uppercase tracking-wider -mt-0.5">Company</span>
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
                        <div className="w-9 h-9 rounded-lg bg-cyan-500/20 flex items-center justify-center">
                            <Building2 className="w-4 h-4 text-cyan-400" />
                        </div>
                        <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium text-white truncate">TechCorp India</div>
                            <div className="text-xs text-white/40 truncate">Enterprise Plan</div>
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
                            <h1 className="text-xl font-semibold text-white">Company Dashboard</h1>
                            <p className="text-sm text-white/40 mt-0.5">Manage your organization</p>
                        </div>
                        <button className="btn-primary text-sm py-2 px-4">
                            + Add HR User
                        </button>
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

                    {/* HR Users Table */}
                    <div className="card p-5">
                        <div className="flex items-center justify-between mb-5">
                            <h2 className="text-base font-semibold text-white">HR Team Members</h2>
                            <span className="text-sm text-white/40">{hrUsers.length} users</span>
                        </div>

                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-white/5">
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">User</th>
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Role</th>
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Verifications</th>
                                    <th className="text-left text-xs font-medium text-white/40 uppercase pb-3">Status</th>
                                    <th className="text-right text-xs font-medium text-white/40 uppercase pb-3">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {hrUsers.map((user) => (
                                    <tr key={user.id} className="group hover:bg-white/[0.02]">
                                        <td className="py-3">
                                            <div className="flex items-center gap-3">
                                                <div className="w-8 h-8 rounded-full bg-cyan-500/20 flex items-center justify-center text-xs text-white font-medium">
                                                    {user.name.split(' ').map(n => n[0]).join('')}
                                                </div>
                                                <div>
                                                    <div className="text-sm font-medium text-white">{user.name}</div>
                                                    <div className="text-xs text-white/40">{user.email}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="py-3 text-sm text-white/60">{user.role}</td>
                                        <td className="py-3">
                                            <span className="text-sm font-medium text-white">{user.verifications}</span>
                                        </td>
                                        <td className="py-3">
                                            <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded text-xs font-medium text-emerald-400 bg-emerald-500/10">
                                                <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                                                {user.status}
                                            </span>
                                        </td>
                                        <td className="py-3 text-right">
                                            <button className="text-sm text-cyan-400 hover:text-cyan-300 font-medium opacity-0 group-hover:opacity-100 transition-opacity">
                                                Manage
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
