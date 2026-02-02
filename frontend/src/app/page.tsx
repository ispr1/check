'use client';

import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, Shield, Zap, Eye, BarChart3, CheckCircle2 } from 'lucide-react';
import Link from 'next/link';

const features = [
  {
    icon: Shield,
    title: 'Government-Verified Identity',
    description: 'Direct integration with Aadhaar, PAN, and UAN APIs for instant verification.',
    color: 'text-indigo-400',
    bg: 'bg-indigo-500/10',
  },
  {
    icon: Eye,
    title: 'Biometric Face Match',
    description: 'AWS Rekognition-powered face comparison with 99.9% accuracy.',
    color: 'text-cyan-400',
    bg: 'bg-cyan-500/10',
  },
  {
    icon: BarChart3,
    title: 'Explainable Trust Score',
    description: 'Transparent 0-100 scoring with detailed breakdown of deductions.',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
  },
  {
    icon: Zap,
    title: 'Document Intelligence',
    description: 'AI-powered forensic analysis detects manipulated documents.',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10',
  },
];

const stats = [
  { value: '2.5M+', label: 'Verifications' },
  { value: '99.2%', label: 'Accuracy' },
  { value: '500+', label: 'Enterprises' },
  { value: '<30s', label: 'Avg Time' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 diamond-pattern opacity-50" />
      <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-indigo-500/10 rounded-full blur-[180px]" />
      <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-purple-500/8 rounded-full blur-[150px]" />

      {/* Navigation */}
      <nav className="relative z-20 w-full px-6 lg:px-12 py-5 flex items-center justify-between border-b border-white/5">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-col">
            <span className="text-lg font-semibold text-white">Kovanent</span>
            <span className="text-[10px] text-indigo-400 uppercase tracking-widest -mt-1">Identity</span>
          </div>
        </Link>

        <div className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-sm text-white/50 hover:text-white transition-colors">Features</a>
          <a href="#pricing" className="text-sm text-white/50 hover:text-white transition-colors">Pricing</a>
          <a href="#docs" className="text-sm text-white/50 hover:text-white transition-colors">Docs</a>
        </div>

        <div className="flex items-center gap-4">
          <Link href="/login" className="text-sm text-white/60 hover:text-white transition-colors font-medium">
            Sign In
          </Link>
          <Link href="/login" className="btn-primary text-sm py-2.5 px-5 flex items-center gap-2">
            Get Started <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 px-6 lg:px-12 pt-20 lg:pt-32 pb-20">
        <div className="max-w-5xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-sm text-white/60 mb-8">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Enterprise-Grade Verification Platform
            </div>

            {/* Headline */}
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
              The Identity
              <br />
              <span className="bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                Verification Platform
              </span>
            </h1>

            {/* Subheadline */}
            <p className="text-lg md:text-xl text-white/50 max-w-2xl mx-auto mb-10 leading-relaxed">
              Verify candidates in under 30 seconds with explainable Trust Scores.
              Reduce hiring fraud by 90% with AI-powered document analysis.
            </p>

            {/* CTAs */}
            <div className="flex items-center justify-center gap-4 mb-16">
              <Link href="/login" className="btn-primary py-3.5 px-8 text-base flex items-center gap-2">
                Start Free Trial <ArrowRight className="w-5 h-5" />
              </Link>
              <Link href="#demo" className="btn-secondary py-3.5 px-8 text-base">
                Schedule Demo
              </Link>
            </div>

            {/* Stats */}
            <div className="flex items-center justify-center gap-10 lg:gap-16 flex-wrap">
              {stats.map((stat) => (
                <div key={stat.label} className="text-center">
                  <div className="text-2xl lg:text-3xl font-bold text-white mb-1">{stat.value}</div>
                  <div className="text-sm text-white/40">{stat.label}</div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 px-6 lg:px-12 py-20 border-t border-white/5">
        <div className="max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Verification, Reimagined
            </h2>
            <p className="text-lg text-white/50 max-w-lg mx-auto">
              Every feature designed to eliminate hiring fraud and accelerate onboarding.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card p-6 hover:bg-[#151520] hover:border-white/10 transition-all"
              >
                <div className={`w-12 h-12 rounded-xl ${feature.bg} flex items-center justify-center mb-5`}>
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-sm text-white/40 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 px-6 lg:px-12 py-20">
        <div className="max-w-3xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="card p-10 lg:p-16"
          >
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Ready to eliminate hiring fraud?
            </h2>
            <p className="text-white/50 mb-8 max-w-md mx-auto">
              Join 500+ enterprises using Kovanent Identity to verify candidates with confidence.
            </p>
            <Link href="/login" className="btn-primary py-3.5 px-8 inline-flex items-center gap-2">
              Start Your Free Trial <ArrowRight className="w-5 h-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 px-6 lg:px-12 py-8 border-t border-white/5">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-indigo-500" />
            <span className="text-sm text-white/30">© 2026 Kovanent Identity</span>
          </div>
          <div className="flex items-center gap-6 text-sm text-white/30">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
