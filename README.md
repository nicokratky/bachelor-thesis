# Bachelor Thesis

> Enabling K8ssandra for Diagonal Elasticity Using the Polaris SLO Framework

## Abstract

Cloud computing has risen immensly in popularity over the recent years. Properties such as elasticity and pay-as-you-go pricing models have motivated customers to reconsider their workload deployment models. To define performance expectations, cloud service providers use Service Level Objectives (SLOs). Most SLOs rely on low-level metrics and are tightly coupled to a specific scaling strategy, such as horizontal scaling. The Polaris SLO tackles these issues by introducing high-level SLOs that are loosely coupled to elasticity (scaling) strategies. This thesis presents a diagonal elasticity strategy for Apache Cassandra. Diagonal elasticity is defined as a combination of vertical and horizontal elasticity. The different components that are necessary to achieve this are introduced. Finally the result is evaluated and compared to using vertical or horizontal elasticity alone. This evaluation shows that using diagonal elasticity for Cassandra it is possible to increase resource efficiency by scaling vertically while also increasing throughput by adding nodes to the cluster when demand is high.
