# Overview

Kèo Sư is a professional Vietnamese football betting website that provides betting odds, match analysis, and betting tips. The platform serves as an official partner of MelBet in Vietnam, offering users comprehensive football betting information including daily betting odds ("kèo thơm"), match analysis, betting strategies, and live scores. The website features a content management system for publishing articles across different categories and includes integration with MelBet's affiliate program.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-rendered architecture with Flask templates and Bootstrap for responsive design. The frontend is built with:
- **Template Engine**: Jinja2 templates with a base layout system for consistent UI
- **Styling**: Bootstrap 5 with custom CSS using a yellow (#ffd700) and black (#0d0d0d) color scheme matching MelBet branding
- **JavaScript**: Vanilla JavaScript for interactive features including chatbot integration, lazy loading, and form enhancements
- **Responsive Design**: Mobile-first approach with Bootstrap's grid system

## Backend Architecture
The backend follows the Flask application pattern with clear separation of concerns:
- **Web Framework**: Flask with SQLAlchemy ORM for database operations
- **Database Models**: Article, Category, BettingOdd, and Match models with proper relationships
- **Form Handling**: WTForms for form validation and rendering
- **Route Organization**: Separate routes.py file handling all URL endpoints
- **SEO Utilities**: Dedicated module for meta tag generation and structured data

## Content Management System
The platform includes a basic CMS for article management:
- **Article Creation**: Form-based article creation with rich content support
- **Category Management**: Predefined categories including "Kèo thơm", "Soi kèo", "Mẹo cược", and "Tin tức"
- **SEO Features**: Meta title, description, and keywords for each article
- **Publishing System**: Draft and published states with featured article support

## Database Design
Uses SQLAlchemy with the following key models:
- **Category**: Stores article categories with slugs and descriptions
- **Article**: Main content model with SEO fields, view tracking, and category relationships
- **BettingOdd**: Stores betting odds data for matches with home/away/draw odds
- **Match**: Stores match information including teams, dates, and scores

## URL Structure and SEO
The application implements SEO-friendly URLs and comprehensive SEO features:
- **Friendly URLs**: Category-based routing (e.g., /keo-thom, /soi-keo)
- **Slug Generation**: Vietnamese character normalization for URL-safe slugs
- **Meta Tags**: Dynamic generation of title, description, and Open Graph tags
- **Sitemap Generation**: Automated sitemap.xml creation for search engines

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web framework with SQLAlchemy for ORM functionality
- **WTForms**: Form handling and validation
- **Werkzeug**: WSGI utilities and middleware

## Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **Custom CSS**: Yellow and black theme matching MelBet branding

## Database
- **SQLite**: Default database for local development (configurable via DATABASE_URL environment variable)
- **PostgreSQL**: Production database support through SQLAlchemy

## Third-party Integrations
- **MelBet Affiliate Program**: Marketing integration and partnership links
- **Udify Chatbot**: Embedded chatbot iframe (https://udify.app/chatbot/xhJuB06Ye6hfb3s5)
- **Live Score Services**: Integration with Flashscore.vn and 7M Sports for real-time match data
- **Vietnamese Sports Data**: Local sports content and betting odds

## Deployment and Environment
- **Replit Compatibility**: Designed to run directly on Replit platform
- **Environment Configuration**: Uses environment variables for database URL and session secrets
- **Static File Handling**: Flask's static file serving for CSS, JavaScript, and images