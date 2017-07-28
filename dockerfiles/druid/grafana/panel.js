{
  "__inputs": [
    {
      "name": "DS_DRUID",
      "label": "druid",
      "description": "",
      "type": "datasource",
      "pluginId": "abhisant-druid-datasource",
      "pluginName": "Druid"
    }
  ],
  "__requires": [
    {
      "type": "datasource",
      "id": "abhisant-druid-datasource",
      "name": "Druid",
      "version": "0.0.4"
    },
    {
      "type": "grafana",
      "id": "grafana",
      "name": "Grafana",
      "version": "4.1.2"
    },
    {
      "type": "panel",
      "id": "graph",
      "name": "Graph",
      "version": ""
    }
  ],
  "annotations": {
    "list": []
  },
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "hideControls": false,
  "id": null,
  "links": [],
  "rows": [
    {
      "collapse": false,
      "height": "250px",
      "panels": [
        {
          "aliasColors": {},
          "bars": true,
          "datasource": "${DS_DRUID}",
          "fill": 1,
          "id": 1,
          "legend": {
            "avg": false,
            "current": false,
            "max": false,
            "min": false,
            "show": true,
            "total": false,
            "values": false
          },
          "lines": false,
          "linewidth": 1,
          "links": [],
          "nullPointMode": "null",
          "percentage": false,
          "pointradius": 5,
          "points": false,
          "renderer": "flot",
          "seriesOverrides": [],
          "span": 12,
          "stack": true,
          "steppedLine": false,
          "targets": [
            {
              "aggregators": [
                {
                  "fieldName": "count",
                  "name": "count",
                  "type": "doubleSum"
                }
              ],
              "currentAggregator": {
                "type": "count"
              },
              "currentFilter": {
                "type": "selector"
              },
              "currentPostAggregator": {
                "fn": "+",
                "type": "arithmetic"
              },
              "currentSelect": {
                "dimension": "",
                "metric": ""
              },
              "customGranularity": "minute",
              "dimension": "domain",
              "druidDS": "domains",
              "druidMetric": "count",
              "errors": {
                "aggregators": "You must supply at least one aggregator"
              },
              "limit": 5,
              "queryType": "topN",
              "refId": "A",
              "shouldOverrideGranularity": false
            }
          ],
          "thresholds": [],
          "timeFrom": "10m",
          "timeShift": null,
          "title": "Top 5 Domains",
          "tooltip": {
            "shared": false,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "name": null,
            "show": true,
            "values": []
          },
          "yaxes": [
            {
              "format": "short",
              "label": null,
              "logBase": 1,
              "max": null,
              "min": null,
              "show": true
            },
            {
              "format": "short",
              "label": null,
              "logBase": 1,
              "max": null,
              "min": null,
              "show": true
            }
          ]
        }
      ],
      "repeat": null,
      "repeatIteration": null,
      "repeatRowId": null,
      "showTitle": false,
      "title": "Dashboard Row",
      "titleSize": "h6"
    },
    {
      "collapse": false,
      "height": 250,
      "panels": [
        {
          "aliasColors": {},
          "bars": false,
          "datasource": "${DS_DRUID}",
          "fill": 1,
          "id": 2,
          "legend": {
            "avg": false,
            "current": false,
            "max": false,
            "min": false,
            "show": true,
            "total": false,
            "values": false
          },
          "lines": true,
          "linewidth": 1,
          "links": [],
          "nullPointMode": "null",
          "percentage": false,
          "pointradius": 5,
          "points": false,
          "renderer": "flot",
          "seriesOverrides": [],
          "span": 12,
          "stack": false,
          "steppedLine": false,
          "targets": [
            {
              "aggregators": [
                {
                  "fieldName": "count",
                  "name": "querys",
                  "type": "longSum"
                }
              ],
              "currentAggregator": {
                "type": "count"
              },
              "currentFilter": {
                "type": "selector"
              },
              "currentPostAggregator": {
                "fn": "+",
                "type": "arithmetic"
              },
              "currentSelect": {
                "dimension": "",
                "metric": ""
              },
              "customGranularity": "minute",
              "druidDS": "domains",
              "errors": {
                "aggregators": "You must supply at least one aggregator"
              },
              "limit": 5,
              "queryType": "timeseries",
              "refId": "A"
            }
          ],
          "thresholds": [],
          "timeFrom": "10m",
          "timeShift": null,
          "title": "QPM",
          "tooltip": {
            "shared": true,
            "sort": 0,
            "value_type": "individual"
          },
          "type": "graph",
          "xaxis": {
            "mode": "time",
            "name": null,
            "show": true,
            "values": []
          },
          "yaxes": [
            {
              "format": "short",
              "label": null,
              "logBase": 1,
              "max": null,
              "min": null,
              "show": true
            },
            {
              "format": "short",
              "label": null,
              "logBase": 1,
              "max": null,
              "min": null,
              "show": true
            }
          ]
        }
      ],
      "repeat": null,
      "repeatIteration": null,
      "repeatRowId": null,
      "showTitle": false,
      "title": "Dashboard Row",
      "titleSize": "h6"
    }
  ],
  "schemaVersion": 14,
  "style": "dark",
  "tags": [],
  "templating": {
    "list": []
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": [
      "5s",
      "10s",
      "30s",
      "1m",
      "5m",
      "15m",
      "30m",
      "1h",
      "2h",
      "1d"
    ],
    "time_options": [
      "5m",
      "15m",
      "1h",
      "6h",
      "12h",
      "24h",
      "2d",
      "7d",
      "30d"
    ]
  },
  "timezone": "browser",
  "title": "New dashboard Copy",
  "version": 3
}