# dashboard.py - HR Analytics Visualization Dashboard
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

DB = 'hr_analytics.db'
sns.set_theme(style='darkgrid', palette='muted')


def load(conn, sql):
    return pd.read_sql_query(sql, conn)


def main():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query('SELECT * FROM employees', conn)

    fig = plt.figure(figsize=(18, 12), facecolor='#0f172a')
    fig.suptitle('HR Analytics Dashboard', fontsize=22, color='white', fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)
    ax_style = dict(facecolor='#1e293b')
    text_style = dict(color='white')

    # 1. Attrition by Department
    ax1 = fig.add_subplot(gs[0, 0], **ax_style)
    att = df.groupby('department')['attrition'].apply(lambda x: (x == 'Yes').mean() * 100).sort_values(ascending=False)
    colors = ['#ef4444' if v > 20 else '#f59e0b' if v > 12 else '#22c55e' for v in att]
    att.plot(kind='barh', ax=ax1, color=colors)
    ax1.set_title('Attrition Rate by Department', **text_style, fontweight='bold')
    ax1.tick_params(colors='white')
    ax1.set_xlabel('Attrition %', color='white')
    for spine in ax1.spines.values(): spine.set_edgecolor('#334155')

    # 2. Salary Distribution
    ax2 = fig.add_subplot(gs[0, 1], **ax_style)
    sal = df.groupby('department')['salary'].mean().sort_values()
    sal.plot(kind='barh', ax=ax2, color='#6366f1')
    ax2.set_title('Avg Salary by Department', **text_style, fontweight='bold')
    ax2.tick_params(colors='white')
    ax2.set_xlabel('Avg Salary ($)', color='white')
    for spine in ax2.spines.values(): spine.set_edgecolor('#334155')

    # 3. Performance vs Satisfaction
    ax3 = fig.add_subplot(gs[0, 2], **ax_style)
    left = df[df['attrition'] == 'Yes']
    stayed = df[df['attrition'] == 'No']
    ax3.scatter(stayed['satisfaction_score'], stayed['performance_score'], alpha=0.4, c='#22c55e', s=15, label='Stayed')
    ax3.scatter(left['satisfaction_score'], left['performance_score'], alpha=0.6, c='#ef4444', s=15, label='Left')
    ax3.set_title('Performance vs Satisfaction', **text_style, fontweight='bold')
    ax3.set_xlabel('Satisfaction Score', color='white')
    ax3.set_ylabel('Performance Score', color='white')
    ax3.tick_params(colors='white')
    ax3.legend(facecolor='#334155', labelcolor='white')
    for spine in ax3.spines.values(): spine.set_edgecolor('#334155')

    # 4. Overtime vs Attrition
    ax4 = fig.add_subplot(gs[1, 0], **ax_style)
    ot = df.groupby(['overtime', 'attrition']).size().unstack().fillna(0)
    ot.plot(kind='bar', ax=ax4, color=['#22c55e', '#ef4444'], rot=0)
    ax4.set_title('Overtime vs Attrition', **text_style, fontweight='bold')
    ax4.tick_params(colors='white')
    ax4.set_xlabel('Overtime', color='white')
    ax4.legend(['Stayed', 'Left'], facecolor='#334155', labelcolor='white')
    for spine in ax4.spines.values(): spine.set_edgecolor('#334155')

    # 5. Tenure Distribution
    ax5 = fig.add_subplot(gs[1, 1], **ax_style)
    ax5.hist(df['years_at_company'], bins=15, color='#a855f7', edgecolor='#0f172a')
    ax5.set_title('Employee Tenure Distribution', **text_style, fontweight='bold')
    ax5.set_xlabel('Years at Company', color='white')
    ax5.set_ylabel('Count', color='white')
    ax5.tick_params(colors='white')
    for spine in ax5.spines.values(): spine.set_edgecolor('#334155')

    # 6. Headcount by Department
    ax6 = fig.add_subplot(gs[1, 2], **ax_style)
    hc = df['department'].value_counts()
    wedgeprops = dict(width=0.5, edgecolor='#0f172a')
    ax6.pie(hc, labels=hc.index, autopct='%1.0f%%', pctdistance=0.75,
            colors=sns.color_palette('pastel'), textprops={'color': 'white'},
            wedgeprops=wedgeprops)
    ax6.set_title('Headcount by Department', **text_style, fontweight='bold')

    plt.savefig('hr_dashboard.png', dpi=150, bbox_inches='tight', facecolor='#0f172a')
    plt.show()
    print('Dashboard saved as hr_dashboard.png')
    conn.close()


if __name__ == '__main__':
    main()
