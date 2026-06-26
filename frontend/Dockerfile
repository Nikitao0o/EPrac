FROM node:22-alpine AS build

WORKDIR /app
COPY . .

RUN if [ -f package.json ]; then \
      npm ci && npm run build; \
    else \
      mkdir -p dist && \
      printf '%s\n' \
        '<!doctype html>' \
        '<html lang="ru">' \
        '<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>EPrac</title></head>' \
        '<body><main style="font-family: system-ui, sans-serif; max-width: 720px; margin: 48px auto; line-height: 1.5"><h1>EPrac frontend container</h1><p>Замените эту заглушку React/Vite-приложением во frontend.</p></main></body>' \
        '</html>' > dist/index.html; \
    fi

FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
