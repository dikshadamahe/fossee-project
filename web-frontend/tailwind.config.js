/**
 * Tailwind CSS Configuration
 * FOSSEE Scientific Analytics UI - design.md tokens
 * 
 * Design System v1.0
 * - Inter for UI
 * - JetBrains Mono for tables/data
 * - Source Serif 4 for headings (optional)
 */

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // =================================================================
      // COLORS (design.md Section 2)
      // =================================================================
      colors: {
        // Primary Colors
        primary: {
          900: '#0F2A44', // Headers, nav background
          700: '#1B7F79', // Primary actions, links
          600: '#3A4E9F', // Analytics highlight
          DEFAULT: '#1B7F79',
        },
        
        // Semantic Colors
        success: '#2EA043',
        warning: '#D97706',
        error: '#C53030',
        
        // Neutrals
        bg: {
          main: '#F7F9FC',    // App background
          surface: '#FFFFFF', // Cards
        },
        border: '#E2E8F0',
        
        // Text Colors
        text: {
          primary: '#102A43',   // Body text
          secondary: '#486581', // Subtext
          muted: '#829AB1',     // Labels
        },
        
        // Chart Palette
        chart: {
          flowrate: '#1B7F79',
          pressure: '#3A4E9F',
          temperature: '#C53030',
          distribution1: '#1B7F79',
          distribution2: '#3A4E9F',
          distribution3: '#2EA043',
          distribution4: '#D97706',
        },
      },
      
      // =================================================================
      // TYPOGRAPHY (design.md Section 3)
      // =================================================================
      fontFamily: {
        // Primary UI font
        sans: ['Inter', 'Segoe UI', 'Noto Sans', 'system-ui', 'sans-serif'],
        // Data/tables font
        mono: ['JetBrains Mono', 'Consolas', 'Monaco', 'monospace'],
        // Headings (optional serif)
        serif: ['Source Serif 4', 'Georgia', 'Times New Roman', 'serif'],
      },
      
      fontSize: {
        // Scale from design.md Section 3.2
        'h1': ['28px', { lineHeight: '1.3', fontWeight: '600' }],
        'h2': ['22px', { lineHeight: '1.35', fontWeight: '600' }],
        'h3': ['18px', { lineHeight: '1.4', fontWeight: '600' }],
        'body': ['15px', { lineHeight: '1.6', fontWeight: '400' }],
        'small': ['13px', { lineHeight: '1.5', fontWeight: '400' }],
        'mono': ['13px', { lineHeight: '1.5', fontWeight: '500' }],
      },
      
      // =================================================================
      // SPACING (design.md Section 4)
      // =================================================================
      // 4px base unit scale
      spacing: {
        '0.5': '2px',
        '1': '4px',
        '2': '8px',
        '3': '12px',
        '4': '16px',
        '5': '20px',
        '6': '24px',
        '8': '32px',
        '10': '40px',
        '12': '48px',
        '16': '64px',
      },
      
      // =================================================================
      // LAYOUT (design.md Section 4.2)
      // =================================================================
      maxWidth: {
        'container': '1280px',
      },
      
      // =================================================================
      // COMPONENTS (design.md Section 5)
      // =================================================================
      borderRadius: {
        'card': '10px',   // Card radius
        'button': '8px',  // Button radius
        DEFAULT: '6px',
      },
      
      boxShadow: {
        // Lab Panel shadow
        'card': '0 4px 12px rgba(0, 0, 0, 0.06)',
        // Elevated card
        'elevated': '0 8px 24px rgba(0, 0, 0, 0.1)',
        // Focus ring
        'focus': '0 0 0 3px rgba(27, 127, 121, 0.3)',
      },
      
      // =================================================================
      // ANIMATION
      // =================================================================
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'pulse-subtle': 'pulseSubtle 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
}
