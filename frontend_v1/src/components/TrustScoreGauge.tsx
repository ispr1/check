import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import './TrustScoreGauge.css';

interface TrustScoreGaugeProps {
    score: number;
}

export const TrustScoreGauge: React.FC<TrustScoreGaugeProps> = ({ score }) => {
    // Determine color based on score
    const getColor = () => {
        if (score >= 75) return '#22c55e'; // Green
        if (score >= 50) return '#f59e0b'; // Yellow
        return '#ef4444'; // Red
    };

    const data = [
        { name: 'Score', value: score },
        { name: 'Remaining', value: 100 - score },
    ];

    const COLORS = [getColor(), '#e2e8f0'];

    return (
        <div className="trust-score-gauge">
            <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        startAngle={180}
                        endAngle={0}
                        innerRadius={80}
                        outerRadius={110}
                        dataKey="value"
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index]} />
                        ))}
                    </Pie>
                </PieChart>
            </ResponsiveContainer>

            <div className="gauge-score">
                <div className="score-value">{score}</div>
                <div className="score-label">Trust Score</div>
            </div>
        </div>
    );
};
