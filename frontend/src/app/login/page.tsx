'use client';

import { motion } from 'framer-motion';
import { Shield, Building2, Users, ArrowRight, Sparkles } from 'lucide-react';
import Link from 'next/link';

const roles = [
    {
        id: 'super-admin',
        title: 'Super Admin',
        description: 'System-wide administration and platform configuration',
        icon: Shield,
        href: '/login/admin',
        color: 'from-violet-500 to-purple-600',
        iconBg: 'bg-violet-500/10',
        iconColor: 'text-violet-400',
    },
    {
        id: 'company',
        title: 'Company',
        description: 'Manage your organization and verification workflows',
        icon: Building2,
        href: '/login/company',
        color: 'from-blue-500 to-cyan-500',
        iconBg: 'bg-blue-500/10',
        iconColor: 'text-blue-400',
    },
    {
        id: 'hr',
        title: 'HR',
        description: 'Review verifications and make hiring decisions',
        icon: Users,
        href: '/login/hr',
        color: 'from-emerald-500 to-teal-500',
        iconBg: 'bg-emerald-500/10',
        iconColor: 'text-emerald-400',
    },
];

export default function LoginPage() {
    return (
        <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 diamond-pattern opacity-50" />
            <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[150px]" />
            <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-purple-500/8 rounded-full blur-[120px]" />

            {/* Content */}
            <div className="relative z-10 min-h-screen flex flex-col">
                {/* Header */}
                <header className="w-full px-6 py-5 flex items-center justify-between">
                    <Link href="/" className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                            <Sparkles className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex flex-col">
                            <span className="text-lg font-semibold text-white">Kovanent</span>
                            <span className="text-[10px] text-indigo-400 uppercase tracking-widest -mt-1">Identity</span>
                        </div>
                    </Link>

                    <div className="flex items-center gap-3">
                        <span className="text-sm text-white/40">New to Kovanent?</span>
                        <Link href="/register" className="text-sm text-indigo-400 hover:text-indigo-300 font-medium">
                            Request Demo →
                        </Link>
                    </div>
                </header>

                {/* Main */}
                <main className="flex-1 flex items-center justify-center px-6 py-12">
                    <div className="w-full max-w-4xl">
                        {/* Title */}
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5 }}
                            className="text-center mb-12"
                        >
                            <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
                                Select Your Portal
                            </h1>
                            <p className="text-lg text-white/50 max-w-md mx-auto">
                                Choose your role to access the appropriate dashboard
                            </p>
                        </motion.div>

                        {/* Role Cards */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                            {roles.map((role, index) => (
                                <motion.div
                                    key={role.id}
                                    initial={{ opacity: 0, y: 20 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    transition={{ duration: 0.5, delay: 0.1 + index * 0.1 }}
                                >
                                    <Link href={role.href} className="block group">
                                        <div className="card p-6 h-full hover:border-white/10 hover:bg-[#151520] transition-all duration-300 hover:-translate-y-1">
                                            {/* Icon */}
                                            <div className={`w-14 h-14 rounded-xl ${role.iconBg} flex items-center justify-center mb-5`}>
                                                <role.icon className={`w-7 h-7 ${role.iconColor}`} />
                                            </div>

                                            {/* Content */}
                                            <h3 className="text-xl font-semibold text-white mb-2">
                                                {role.title}
                                            </h3>
                                            <p className="text-sm text-white/40 mb-5 leading-relaxed">
                                                {role.description}
                                            </p>

                                            {/* Action */}
                                            <div className="flex items-center text-indigo-400 text-sm font-medium group-hover:text-indigo-300">
                                                <span>Continue</span>
                                                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                                            </div>
                                        </div>
                                    </Link>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </main>

                {/* Footer */}
                <footer className="w-full px-6 py-6 text-center">
                    <p className="text-sm text-white/20">
                        © 2026 Kovanent Identity. All rights reserved.
                    </p>
                </footer>
            </div>
        </div>
    );
}
