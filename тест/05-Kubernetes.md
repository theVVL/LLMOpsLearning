# Глава 5. Kubernetes

> Курс: DevOps + AI. Вопросы 133–169 из 546.
> Нумерация сквозная — не менять, не переставлять.

## Темы блока

- Архитектура Control Plane и worker nodes
- Pod, Deployment, ReplicaSet, StatefulSet, DaemonSet
- Service, Ingress, CoreDNS и CNI
- ConfigMap, Secret, PV/PVC/StorageClass
- Probes, requests/limits и QoS
- Scheduling, RBAC, HPA/PDB, NetworkPolicy
- Отладка подов и обслуживание кластера

---

133•[БАЗА] Зачем нужен Kubernetes, если есть Docker Compose? Какие проблемы крупной инфраструктуры (самолечение, автоклининг, масштабирование на сотни серверов) он решает?

134•[БАЗА] Что такое Kubernetes простыми словами? Подробная архитектура Control Plane (api-server, etcd, scheduler, controller-manager) и устройство Worker Nodes (kubelet, kube-proxy). Как они взаимодействуют при создании нового пода?

135•[БАЗА] Что такое Pod (под)? Зачем внутри пода нужны общий сетевой namespace и localhost между контейнерами, как они делят диски (volumes) и почему под — минимальная единица размещения, а не контейнер?

136•[БАЗА] Что такое база данных etcd в Kubernetes? Почему она является единственным источником правды, как работает ее механизм Watch (наблюдение) и почему с ней общается только API-Server?

137•[БАЗА] Вы ввели команду kubectl get pods и увидели статус Pending, ImagePullBackOff или ErrImagePull. Что означает каждый статус, каковы их системные причины (шедулер не нашёл ноду, неверный тег образа, приватный registry без Secret) и какими командами искать причину?

138•[БАЗА] pause-контейнер и Network Namespace пода. Почему под получает один IP на всех, и как pause держит сеть, даже если приложение упало?

139•[БАЗА] etcd + Watch + Raft. Почему etcd — «единственный источник правды», как кворум Raft защищает от расщепления сознания (split-brain) и почему падение etcd = паралич управления (но запущенные поды живут)?

140•[ДЖУН] kube-scheduler: Filtering → Scoring. Почему под «застревает» в Pending (например, 0/5 nodes are available: 3 Insufficient cpu), и как Scoring выбирает «наименее загруженную» ноду?

141•[ДЖУН] kube-proxy и iptables/IPVS. Почему kube-proxy не «гоняет трафик через себя», а настраивает правила ядра, и чем IPVS быстрее iptables на больших кластерах?

142•[ДЖУН] Вы ввели команду kubectl get pods и увидели статус CrashLoopBackOff или OOMKilled. Как по kubectl describe pod и kubectl logs отличить «приложение падает сразу» (код, конфиг, exit code 1) от «съел память» (exit code 137, limits.memory), и что смотреть в блоке Events?

143•[ДЖУН] ConfigMap vs Secret: почему Base64 — это не шифрование. Почему echo YWRtaW4= | base64 -d = admin, и почему в проде нужен HashiCorp Vault/External Secrets Operator?

144•[ДЖУН] Secret в поде: монтирование через volume против передачи в env-переменные. Что безопаснее, почему секрет из env легко утекает (docker inspect, /proc/self/environ, логи) и зачем нужны immutable Secret и ротация?

145•[ДЖУН] PV / PVC / Volume: «цистерна → талон → шланг». Почему PVC — это «запрос», PV — «реальный диск», и что произойдёт с данными при удалении StatefulSet-пода, если PVC остался?

146•[ДЖУН] В чем разница между ReplicaSet и Deployment? Как именно Deployment управляет обновлением приложения через «ревизии» (ReplicaSet'ы), как посмотреть историю и откатиться (kubectl rollout history/undo)?

147•[ДЖУН] Как обновить приложение в Kubernetes без простоя (Zero Downtime)? Подробный разбор стратегий RollingUpdate (плавная замена с параметрами maxSurge / maxUnavailable) и Recreate (полная перезагрузка).

148•[ДЖУН] Что такое Зонды Доступности? В чем разница в зонах ответственности между Liveness Probe (жив ли контейнер), Readiness Probe (готов ли принимать трафик) и Startup Probe (загрузился ли контейнер)?

149•[ДЖУН] Сетевой доступ внутри кластера: зачем нужна сущность Service? В чем разница между типами ClusterIP (внутрикластерный), NodePort (открытие портов на нодах) и LoadBalancer (интеграция с облачным балансировщиком)?

150•[ДЖУН] Что такое Ingress и Ingress-контроллер (на примере Nginx Ingress)? Как они маршрутизируют внешний L7-трафик (домены, пути) к внутренним сервисам кластера?

151•[ДЖУН] requests/limits и QoS-классы: чем request отличается от limit, как на основе них под получает Guaranteed/Burstable/BestEffort и почему при OOMKilled виноват limit, а при Pending — request?

152•[ДЖУН] RBAC и ServiceAccount: как устроены Role/ClusterRole и RoleBinding/ClusterRoleBinding, зачем поду ServiceAccount-токен и как проверить права через kubectl auth can-i?

153•[ДЖУН] taints/tolerations, nodeSelector и affinity: как запретить планировать поды на ноду (taint), как разрешить (toleration) и чем nodeAffinity/podAntiAffinity помогают разнести реплики по разным зонам?

154•[ДЖУН] Job и CronJob: чем Job отличается от пода и Deployment, как работают completions/parallelism и что делать, если CronJob «наслаивает» запуски (concurrencyPolicy, startingDeadlineSeconds)?

155•[ДЖУН] Helm простыми словами: зачем нужен пакетный менеджер (чарт, values.yaml, шаблоны, релизы и история), как helm rollback спасает и почему «Helm-магия» иногда хуже чистого Kustomize?

156•[МИДЛ] Жизненный цикл пода (Pod Lifecycle): разбор состояний Pending, Running, Succeeded, Failed и Unknown. Что такое restartPolicy (Always/OnFailure/Never) и как работает BackOff-таймер, из-за которого появляется CrashLoopBackOff?

157•[МИДЛ] В чем разница между базовыми контроллерами управления подами: Deployment (для stateless-приложений), StatefulSet (для баз данных и приложений со стейтом) и DaemonSet (для системных агентов логирования/мониторинга)?

158•[МИДЛ] Как устроена сеть в K8s на базовом уровне? Что такое спецификация CNI (Container Network Interface), как поды получают уникальные IP-адреса и в чем разница между плагинами Flannel (простой оверлей/VXLAN) и Calico (маршрутизация через BGP и гибкие сетевые политики)?

159•[МИДЛ] Как работает внутренний DNS-сервер кластера (CoreDNS)? Как поды находят друг друга по имени сервиса внутри одного пространства имен (namespace) и за его пределами?

160•[МИДЛ] Продвинутая маршрутизация трафика: в чем разница между классическим Nginx Ingress и Ingress-контроллером на базе Traefik? Что такое middleware, IngressRoute CRD и в каких случаях Traefik удобнее Nginx?

161•[МИДЛ] Как устроена подсистема хранения данных в K8s? Что такое StorageClass и Dynamic Provisioning, как по PVC автоматически создаётся PV, и как reclaimPolicy (Delete/Retain) определяет судьбу данных после удаления заявки?

162•[МИДЛ] Продвинутый шедулинг: по какому алгоритму работает kube-scheduler? Из каких этапов состоят процессы фильтрации (Filtering) и подсчета очков (Scoring) при выборе ноды для пода?

163•[МИДЛ] Концепция Service Mesh (Istio / Linkerd): Зачем добавлять Sidecar-контейнер (Envoy proxy) к каждому поду? Какие проблемы безопасности (шифрование mTLS между подами) и трассировки трафика это решает?

164•[МИДЛ] Сценарии масштабирования и деплоя в K8s: глубокая физика инкрементальных изменений и пошаговый процесс взаимодействия компонентов при выполнении команд kubectl apply или kubectl scale.

165•[МИДЛ] Ingress vs Ingress Controller vs LoadBalancer Service. Почему 20 микросервисов = 20 LoadBalancer = дорого, и как один Ingress (Nginx/Traefik) с правилами my-shop.com/backend → backend-service решает это?

166•[МИДЛ] HPA/VPA и PodDisruptionBudget: как HPA масштабирует по CPU/памяти/кастомным метрикам, почему VPA часто конфликтует с HPA, и зачем PDB, чтобы drain ноды не убил все реплики сразу?

167•[МИДЛ] NetworkPolicy: как в K8s ограничить трафик между подами (default deny, allow по labels/namespace/port) и почему без CNI, поддерживающего политики (Calico/Cilium), манифест просто игнорируется?

168•[МИДЛ] Бэкап и восстановление etcd: почему etcd snapshot — единственный способ восстановить состояние кластера (а не манифесты подов), как снять snapshot через etcdctl и что происходит с подами после restore?

169•[МИДЛ] Обслуживание нод: как kubectl drain/cordon выводят ноду из работы без потери подов (PDB, DaemonSet'ы, поды с local-storage) и как проходит upgrade кластера по одной ноде?
