# Diagrammes du Projet

Copiez-collez ces codes dans un éditeur Mermaid (ex: [Mermaid Live Editor](https://mermaid.live/)) pour générer les images pour vos slides.

## 1. Slide 6 : Pipeline de Données (ETL)

```mermaid
graph LR
    subgraph Raw Data
    A[Yield CSV] --> M(Merge)
    B[Rain CSV] --> M
    C[Temp CSV] --> M
    D[Pesticides CSV] --> M
    end

    M --> E{Cleaning}
    E --> F[Feature Eng.]
    
    subgraph Processing
    F --> G(StandardScaler)
    F --> H(OneHotEncoder)
    end

    G --> I[Merged Data Ready]
    H --> I
```

## 2. Slide 12 : Architecture MLOps (End-to-End)

```mermaid
flowchart TD
    subgraph Dev Laptop
        A[Code & Test] -->|Git Push| B(GitHub Repo)
    end

    subgraph CI/CD Pipeline
        B --> C{GitHub Actions}
        C -->|pytest| D[Unit Tests]
        D -->|Success| E[Build Docker Image]
        E -->|Push| F[Docker Registry]
    end

    subgraph Production
        F -->|Pull| G[Container FastAPI]
        G --> H[Streamlit App]
    end
```
