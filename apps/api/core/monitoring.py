"""
Monitoring and analytics configuration
"""
import logging
from django.conf import settings

# Configure logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/jan-gan-tantra/app.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/jan-gan-tantra/error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'wiki': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'govgraph': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'issues': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'ai': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}


# Metrics to track
METRICS_CONFIG = {
    'api_response_time': {
        'type': 'histogram',
        'description': 'API endpoint response times',
        'buckets': [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    },
    'api_requests_total': {
        'type': 'counter',
        'description': 'Total API requests by endpoint and status'
    },
    'active_users': {
        'type': 'gauge',
        'description': 'Number of active users in last 24 hours'
    },
    'issues_reported': {
        'type': 'counter',
        'description': 'Total issues reported'
    },
    'solutions_viewed': {
        'type': 'counter',
        'description': 'Total solution views'
    },
    'ai_requests': {
        'type': 'counter',
        'description': 'AI service requests by type'
    },
    'translation_requests': {
        'type': 'counter',
        'description': 'Translation requests by language pair'
    },
    'voice_transcriptions': {
        'type': 'counter',
        'description': 'Voice transcription requests'
    },
}


# Health check endpoints
HEALTH_CHECKS = {
    'database': {
        'check': 'django_health_check.db.backends.DatabaseBackend',
        'critical': True
    },
    'redis': {
        'check': 'django_health_check.cache.backends.CacheBackend',
        'critical': True
    },
    'storage': {
        'check': 'django_health_check.storage.backends.DefaultFileStorageHealthCheck',
        'critical': False
    },
}


# Alert thresholds
ALERT_THRESHOLDS = {
    'api_error_rate': 0.05,  # 5% error rate
    'api_response_time_p95': 2.0,  # 2 seconds
    'database_connections': 80,  # 80% of max connections
    'memory_usage': 0.85,  # 85% memory usage
    'disk_usage': 0.90,  # 90% disk usage
}


# Analytics events to track
ANALYTICS_EVENTS = [
    'user_signup',
    'solution_viewed',
    'solution_upvoted',
    'issue_reported',
    'issue_upvoted',
    'officer_contacted',
    'translation_used',
    'voice_search_used',
    'ai_jargon_simplified',
    'complaint_drafted',
    'rti_generated',
]
