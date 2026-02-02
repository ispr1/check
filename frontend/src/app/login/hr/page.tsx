'use client';

import { motion } from 'framer-motion';
import { Users, ArrowLeft, Eye, EyeOff, Sparkles } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function HRLoginPage() {
    const router = useRouter();
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');

        try {
            const response = await fetch('http://localhost:8000/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: email,
                    password: password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                router.push('/hr/dashboard');
            } else {
                setError('Invalid credentials. Please try again.');
            }
        } catch {
            setError('Unable to connect to server. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden flex items-center justify-center px-4">
            {/* Background */}
            <div className="absolute inset-0 diamond-pattern opacity-50" />
            <div className="absolute top-1/3 right-1/3 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[150px]" />

            {/* Back Link */}
            <Link
                href="/login"
                className="absolute top-6 left-6 flex items-center gap-2 text-white/40 hover:text-white transition-colors z-20"
            >
                <ArrowLeft className="w-4 h-4" />
                <span className="text-sm">Back to portals</span>
            </Link>

            {/* Login Card */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="relative z-10 w-full max-w-md"
            >
                <div className="card p-8">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 flex items-center justify-center mx-auto mb-5">
                            <Users className="w-8 h-8 text-emerald-400" />
                        </div>
                        <h1 className="text-2xl font-bold text-white mb-2">HR Portal</h1>
                        <p className="text-white/40 text-sm">Review verifications and make decisions</p>
                    </div>

                    {/* Error */}
                    {error && (
                        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center">
                            {error}
                        </div>
                    )}

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="block text-sm font-medium text-white/60 mb-2">
                                Work Email
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="input"
                                placeholder="hr@yourcompany.com"
                                required
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-white/60 mb-2">
                                Password
                            </label>
                            <div className="relative">
                                <input
                                    type={showPassword ? 'text' : 'password'}
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="input pr-12"
                                    placeholder="••••••••"
                                    required
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-4 top-1/2 -translate-y-1/2 text-white/30 hover:text-white/60 transition-colors"
                                >
                                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                                </button>
                            </div>
                        </div>

                        <div className="flex items-center justify-between text-sm pt-1">
                            <label className="flex items-center gap-2 text-white/40 cursor-pointer">
                                <input type="checkbox" className="w-4 h-4 rounded bg-white/5 border-white/10" />
                                <span>Remember me</span>
                            </label>
                            <a href="#" className="text-emerald-400 hover:text-emerald-300">
                                Forgot password?
                            </a>
                        </div>

                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-semibold py-3 rounded-xl hover:shadow-lg hover:shadow-emerald-500/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                        >
                            {isLoading ? (
                                <>
                                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                    <span>Signing in...</span>
                                </>
                            ) : (
                                <span>Sign In</span>
                            )}
                        </button>
                    </form>

                    {/* Footer */}
                    <div className="mt-6 pt-6 border-t border-white/5 text-center">
                        <p className="text-white/30 text-xs">
                            Access provided by your company administrator
                        </p>
                    </div>
                </div>

                {/* Logo */}
                <div className="flex items-center justify-center gap-2 mt-8">
                    <Sparkles className="w-4 h-4 text-emerald-500" />
                    <span className="text-sm text-white/30">Kovanent Identity</span>
                </div>
            </motion.div>
        </div>
    );
}
