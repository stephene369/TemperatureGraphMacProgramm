// Variables globales
let documentationSections = [];
let currentSection = null;

// Chargement de la page de documentation
function loadDocumentationPage() {
    showLoading('Chargement de la documentation...');
    
    // Charger les sections de documentation
    documentationSections = [
        {
            id: "intro",
            title: "Introduction",
            icon: "bx bx-info-circle text-blue-500",
            content: `
                <div class="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:scale-[1.01] hover:shadow-md">
                    <p class="mb-4 leading-relaxed">ClimaGraph est une application d'analyse de données climatiques qui vous permet de visualiser et d'analyser les données de température et d'humidité provenant de différents capteurs.</p>
                    <p class="mb-4">Cette documentation vous guidera à travers les différentes fonctionnalités de l'application et vous expliquera comment les utiliser efficacement.</p>
                </div>
                
                <div class="flex justify-center my-6 animate__animated animate__pulse animate__infinite animate__slower">
                    <img src="assets/img/logo.png" alt="ClimaGraph Logo" class="w-32 h-32 drop-shadow-lg">
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
                    <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg border-l-4 border-green-500 transform transition-all duration-300 hover:shadow-md">
                        <h4 class="font-semibold mb-2 flex items-center"><i class='bx bx-line-chart text-green-500 mr-2'></i> Visualisation</h4>
                        <p class="text-sm">Créez des graphiques interactifs pour visualiser vos données climatiques.</p>
                    </div>
                    
                    <div class="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg border-l-4 border-purple-500 transform transition-all duration-300 hover:shadow-md">
                        <h4 class="font-semibold mb-2 flex items-center"><i class='bx bx-analyse text-purple-500 mr-2'></i> Analyse</h4>
                        <p class="text-sm">Analysez les tendances et identifiez les anomalies dans vos données.</p>
                    </div>
                    
                    <div class="bg-orange-50 dark:bg-orange-900/30 p-4 rounded-lg border-l-4 border-orange-500 transform transition-all duration-300 hover:shadow-md">
                        <h4 class="font-semibold mb-2 flex items-center"><i class='bx bx-export text-orange-500 mr-2'></i> Exportation</h4>
                        <p class="text-sm">Exportez vos graphiques pour les inclure dans vos rapports.</p>
                    </div>
                </div>
            `
        },
        {
            id: "getting-started",
            title: "Premiers pas",
            icon: "bx bx-walk text-green-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-green-50 to-teal-50 dark:from-green-900/30 dark:to-teal-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">Pour commencer à utiliser ClimaGraph, suivez ces étapes simples :</p>
                </div>
                
                <div class="relative pl-8 pb-8">
                    <!-- Timeline line -->
                    <div class="absolute left-4 top-0 h-full w-0.5 bg-blue-500"></div>
                    
                    <!-- Step 1 -->
                    <div class="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                        <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">1</div>
                        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                            <h4 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Ajoutez vos capteurs</h4>
                            <p class="mb-2">Commencez par ajouter vos capteurs dans la section <strong>Capteurs & Fichiers</strong>.</p>
                            <p class="text-sm text-gray-600 dark:text-gray-400">Donnez un nom significatif à chaque capteur pour faciliter leur identification ultérieure.</p>
                        </div>
                    </div>
                    
                    <!-- Step 2 -->
                    <div class="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                        <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">2</div>
                        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                            <h4 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Associez des fichiers de données</h4>
                            <p class="mb-2">Associez des fichiers de données à vos capteurs en utilisant le bouton <strong>Associer un fichier</strong>.</p>
                            <p class="text-sm text-gray-600 dark:text-gray-400">Formats supportés : Excel (.xlsx, .xls), CSV (.csv), HOBO (.hobo)</p>
                        </div>
                    </div>
                    
                    <!-- Step 3 -->
                    <div class="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                        <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">3</div>
                        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                            <h4 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Mappez les colonnes</h4>
                            <p class="mb-2">Définissez quelles colonnes correspondent à la date, la température, l'humidité et le point de rosée dans la section <strong>Mappage des Colonnes</strong>.</p>
                            <p class="text-sm text-gray-600 dark:text-gray-400">L'application tentera de détecter automatiquement les colonnes, mais vous pouvez les ajuster si nécessaire.</p>
                        </div>
                    </div>
                    
                    <!-- Step 4 -->
                    <div class="relative transform transition-all duration-300 hover:translate-x-1">
                        <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">4</div>
                        <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                            <h4 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Générez des graphiques</h4>
                            <p class="mb-2">Créez différents types de graphiques dans la section <strong>Graphiques</strong> pour visualiser et analyser vos données.</p>
                            <p class="text-sm text-gray-600 dark:text-gray-400">Vous pouvez générer un seul type de graphique ou tous les types en une seule fois.</p>
                        </div>
                    </div>
                </div>
                
                <div class="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg mt-6 border-l-4 border-yellow-500">
                    <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-bulb text-yellow-500 mr-2'></i> Conseil</h5>
                    <p>Avant de commencer, assurez-vous que vos fichiers de données sont bien structurés et contiennent au minimum des colonnes pour la date et la température.</p>
                </div>
            `
        },
        {
            id: "capteurs",
            title: "Capteurs & Fichiers",
            icon: "bx bx-chip text-red-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/30 dark:to-pink-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">La section <strong>Capteurs & Fichiers</strong> vous permet de gérer vos capteurs et les fichiers de données associés.</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                            <i class='bx bx-plus-circle text-xl mr-2'></i> Ajouter un capteur
                        </h4>
                        <ol class="list-decimal list-inside space-y-3 ml-4 mb-4">
                            <li class="pb-2 border-b border-gray-100 dark:border-gray-700">Cliquez sur le bouton <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded font-mono text-sm">Ajouter un capteur</span></li>
                            <li class="pb-2 border-b border-gray-100 dark:border-gray-700">Saisissez un nom pour votre capteur (ex: "Salon", "Chambre", "Extérieur")</li>
                            <li>Cliquez sur <span class="px-2 py-1 bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200 rounded font-mono text-sm">Ajouter</span> pour confirmer</li>
                        </ol>
                        
                        <div class="bg-blue-50 dark:bg-blue-900/30 p-3 rounded-lg">
                            <h5 class="font-semibold mb-1 text-sm flex items-center"><i class='bx bx-info-circle text-blue-500 mr-1'></i> Bonnes pratiques</h5>
                            <ul class="list-disc list-inside text-sm text-gray-700 dark:text-gray-300">
                                <li>Utilisez des noms descriptifs (ex: "Salon Nord", "Chambre Sud")</li>
                                <li>Pour les capteurs extérieurs, incluez "Ext" dans le nom pour qu'ils soient affichés avec des lignes pointillées dans les graphiques</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                            <i class='bx bx-link text-xl mr-2'></i> Associer un fichier
                        </h4>
                        <ol class="list-decimal list-inside space-y-3 ml-4 mb-4">
                            <li class="pb-2 border-b border-gray-100 dark:border-gray-700">Cliquez sur le bouton <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded font-mono text-sm">Associer un fichier</span> à côté du capteur concerné</li>
                            <li class="pb-2 border-b border-gray-100 dark:border-gray-700">Sélectionnez le fichier de données dans l'explorateur de fichiers</li>
                            <li>Attendez que le fichier soit chargé et analysé (une notification de succès s'affichera)</li>
                        </ol>
                        
                        <div class="bg-green-50 dark:bg-green-900/30 p-3 rounded-lg">
                            <h5 class="font-semibold mb-1 text-sm flex items-center"><i class='bx bx-check-circle text-green-500 mr-1'></i> Formats supportés</h5>
                            <ul class="list-disc list-inside text-sm text-gray-700 dark:text-gray-300">
                                <li><strong>Excel</strong> (.xlsx, .xls) - Feuilles de calcul Microsoft Excel</li>
                                <li><strong>CSV</strong> (.csv) - Fichiers de valeurs séparées par des virgules</li>
                                <li><strong>HOBO</strong> (.hobo) - Fichiers exportés depuis les enregistreurs HOBO</li>
                            </ul>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                        <i class='bx bx-trash text-xl mr-2'></i> Supprimer un capteur
                    </h4>
                    <ol class="list-decimal list-inside space-y-3 ml-4 mb-4">
                        <li class="pb-2 border-b border-gray-100 dark:border-gray-700">Cliquez sur le bouton <span class="px-2 py-1 bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200 rounded font-mono text-sm">Supprimer</span> à côté du capteur concerné</li>
                        <li>Confirmez la suppression dans la boîte de dialogue qui apparaît</li>
                    </ol>
                    
                    <div class="bg-red-50 dark:bg-red-900/30 p-3 rounded-lg border-l-4 border-red-500 animate__animated animate__headShake">
                        <h5 class="font-semibold mb-1 flex items-center"><i class='bx bx-error-circle text-red-500 mr-1'></i> Attention</h5>
                        <p class="text-sm text-gray-700 dark:text-gray-300">La suppression d'un capteur est <strong>définitive</strong> et entraîne également la suppression de tous les fichiers et mappages associés. Cette action ne peut pas être annulée.</p>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-3 text-red-600 dark:text-red-400 flex items-center">
                            <i class='bx bx-error-alt text-xl mr-2'></i> Erreurs possibles
                        </h4>
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Fichier non reconnu</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Le format du fichier n'est pas supporté ou le fichier est corrompu.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Vérifiez le format du fichier et assurez-vous qu'il n'est pas endommagé.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Fichier trop volumineux</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Le fichier dépasse la taille maximale autorisée.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Divisez le fichier en plusieurs fichiers plus petits ou supprimez les données non essentielles.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Colonnes manquantes</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Le fichier ne contient pas les colonnes nécessaires (date, température).</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Vérifiez que votre fichier contient au moins des colonnes de date et de température.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-3 text-red-600 dark:text-red-400 flex items-center">
                            <i class='bx bx-bulb text-xl mr-2'></i> Astuces avancées
                        </h4>
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Préparation des fichiers</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Pour faciliter la détection automatique, nommez vos colonnes avec des termes explicites comme "Date", "Température", "Humidité".</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Organisation des capteurs</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Créez un capteur par emplacement physique pour une meilleure organisation et analyse.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Mise à jour des données</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Pour mettre à jour les données d'un capteur, associez simplement un nouveau fichier. L'ancien sera remplacé automatiquement.</p>
                            </div>
                        </div>
                    </div>
                </div>
            `
        },
        {
            id: "mapping",
            title: "Mappage des Colonnes",
            icon: "bx bx-link-alt text-purple-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/30 dark:to-indigo-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">La section <strong>Mappage des Colonnes</strong> vous permet de définir quelles colonnes de vos fichiers correspondent à la date, la température, l'humidité et le point de rosée.</p>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-purple-600 dark:text-purple-400 flex items-center">
                        <i class='bx bx-map-alt text-xl mr-2'></i> Mapper les colonnes
                    </h4>
                    
                    <div class="relative pl-8 pb-8">
                        <!-- Timeline line -->
                        <div class="absolute left-4 top-0 h-full w-0.5 bg-purple-500"></div>
                        
                        <!-- Step 1 -->
                        <div class="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                            <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">1</div>
                            <div class="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                                <h5 class="font-semibold mb-2">Sélectionner un capteur</h5>
                                <p class="text-sm">Choisissez un capteur dans la liste déroulante. Seuls les capteurs avec des fichiers associés sont affichés.</p>
                               
                            </div>
                        </div>
                        
                        <!-- Step 2 -->
                        <div class="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                            <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">2</div>
                            <div class="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                                <h5 class="font-semibold mb-2">Vérifier la détection automatique</h5>
                                <p class="text-sm">L'application tente de détecter automatiquement les colonnes appropriées. Vérifiez si les sélections sont correctes.</p>
                                
                            </div>
                        </div>
                        
                        <!-- Step 3 -->
                        <div class="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                            <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">3</div>
                            <div class="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                                <h5 class="font-semibold mb-2">Ajuster les mappages si nécessaire</h5>
                                <p class="text-sm">Si la détection automatique n'est pas correcte, sélectionnez manuellement les colonnes appropriées :</p>
                                <ul class="list-disc list-inside space-y-2 ml-4 mt-2 text-sm">
                                    <li><strong>Colonne de date</strong> : colonne contenant les dates/heures des mesures <span class="text-red-500">(obligatoire)</span></li>
                                    <li><strong>Colonne de température</strong> : colonne contenant les valeurs de température <span class="text-red-500">(obligatoire)</span></li>
                                    <li><strong>Colonne d'humidité</strong> : colonne contenant les valeurs d'humidité <span class="text-gray-500">(optionnelle)</span></li>
                                    <li><strong>Colonne de point de rosée</strong> : colonne contenant les valeurs de point de rosée <span class="text-gray-500">(optionnelle)</span></li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- Step 4 -->
                        <div class="relative transform transition-all duration-300 hover:translate-x-1">
                            <div class="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">4</div>
                            <div class="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                                <h5 class="font-semibold mb-2">Enregistrer le mappage</h5>
                                <p class="text-sm">Cliquez sur le bouton <span class="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded font-mono text-sm">Enregistrer le mappage</span> pour confirmer vos sélections.</p>
                                <p class="text-sm mt-2">Une notification de succès s'affichera si le mappage a été enregistré correctement.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-purple-600 dark:text-purple-400 flex items-center">
                        <i class='bx bx-table text-xl mr-2'></i> Aperçu des données
                    </h4>
                    <p class="mb-4">Un aperçu des premières lignes de votre fichier est affiché pour vous aider à identifier les colonnes correctes :</p>
                    
                    <div class="overflow-x-auto mb-4">
                        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                            <thead>
                                <tr class="bg-gray-100 dark:bg-gray-700">
                                    <th class="py-2 px-4 border-b text-left">Date</th>
                                    <th class="py-2 px-4 border-b text-left">Température (°C)</th>
                                    <th class="py-2 px-4 border-b text-left">Humidité (%)</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="border-b border-gray-200 dark:border-gray-700">
                                    <td class="py-2 px-4">2023-01-01 08:00:00</td>
                                    <td class="py-2 px-4">21.5</td>
                                    <td class="py-2 px-4">45.2</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700">
                                    <td class="py-2 px-4">2023-01-01 09:00:00</td>
                                    <td class="py-2 px-4">22.1</td>
                                    <td class="py-2 px-4">46.8</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700">
                                    <td class="py-2 px-4">2023-01-01 10:00:00</td>
                                    <td class="py-2 px-4">22.8</td>
                                    <td class="py-2 px-4">47.5</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                        Cet aperçu vous aide à identifier visuellement les colonnes à mapper. Utilisez-le pour vérifier que les données sont correctement formatées.
                    </p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-3 text-purple-600 dark:text-purple-400 flex items-center">
                            <i class='bx bx-error-alt text-xl mr-2'></i> Erreurs possibles
                        </h4>
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Colonnes obligatoires non sélectionnées</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Les colonnes de date et de température sont obligatoires.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Sélectionnez au moins une colonne pour la date et une pour la température.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Format de date non reconnu</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">La colonne de date contient des valeurs dans un format non reconnu.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Vérifiez que votre colonne de date contient des dates valides. Reformatez-les si nécessaire.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Valeurs numériques invalides</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Les colonnes de température ou d'humidité contiennent des valeurs non numériques.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Assurez-vous que ces colonnes ne contiennent que des nombres.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-3 text-purple-600 dark:text-purple-400 flex items-center">
                            <i class='bx bx-bulb text-xl mr-2'></i> Astuces avancées
                        </h4>
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Détection automatique</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">L'application recherche des mots-clés comme "date", "temp", "humid" dans les noms de colonnes. Utilisez des noms explicites pour faciliter la détection.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Point de rosée</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Si votre fichier ne contient pas de colonne de point de rosée, l'application peut la calculer automatiquement à partir de la température et de l'humidité.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Modification ultérieure</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Vous pouvez modifier le mappage à tout moment en revenant à cette section et en sélectionnant le capteur concerné.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg mb-4 border-l-4 border-blue-500 animate__animated animate__pulse animate__infinite animate__slow">
                    <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-info-circle text-blue-500 mr-2'></i> Information importante</h5>
                    <p>Les colonnes de date et de température sont <strong>obligatoires</strong> pour générer des graphiques. Les colonnes d'humidité et de point de rosée sont optionnelles, mais nécessaires pour certains types de graphiques comme l'amplitude hydrique ou le risque de point de rosée.</p>
                </div>
            `
        },
        {
            id: "graphs",
            title: "Graphiques",
            icon: "bx bx-line-chart text-green-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">La section <strong>Graphiques</strong> vous permet de générer différents types de visualisations à partir de vos données climatiques.</p>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-green-600 dark:text-green-400 flex items-center">
                        <i class='bx bx-bar-chart-alt-2 text-xl mr-2'></i> Générer un graphique
                    </h4>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-green-200 dark:border-green-800 pb-2">Étape 1: Sélectionner un type de graphique</h5>
                            <p class="text-sm mb-3">Choisissez le type de graphique que vous souhaitez générer dans la liste déroulante.</p>
                            <div class="p-2 bg-white dark:bg-gray-800 rounded border border-green-200 dark:border-green-800">
                                <select class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                                    <option value="all">Tous les types de graphiques</option>
                                    <option value="temperature_time">Température en fonction du temps</option>
                                    <option value="humidity_time">Humidité en fonction du temps</option>
                                    <option value="temperature_amplitude">Amplitude thermique quotidienne</option>
                                    <option value="humidity_amplitude">Amplitude hydrique quotidienne</option>
                                    <option value="humidity_profile">Profil d'humidité par capteur</option>
                                    <option value="dew_point_risk">Risque de point de rosée</option>
                                </select>
                            </div>
                            <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">L'option "Tous les types de graphiques" générera automatiquement tous les graphiques disponibles.</p>
                        </div>
                        
                        <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-green-200 dark:border-green-800 pb-2">Étape 2: Sélectionner les capteurs</h5>
                            <p class="text-sm mb-3">Cochez un ou plusieurs capteurs à inclure dans le graphique.</p>
                            <div class="p-2 bg-white dark:bg-gray-800 rounded border border-green-200 dark:border-green-800 max-h-32 overflow-y-auto">
                                <div class="flex items-center mb-2">
                                    <input type="checkbox" id="capteur-1" class="mr-2">
                                    <label for="capteur-1">Salon</label>
                                </div>
                                <div class="flex items-center mb-2">
                                    <input type="checkbox" id="capteur-2" class="mr-2">
                                    <label for="capteur-2">Chambre</label>
                                </div>
                                <div class="flex items-center">
                                    <input type="checkbox" id="capteur-3" class="mr-2">
                                    <label for="capteur-3">Extérieur</label>
                                </div>
                            </div>
                            <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">Pour une meilleure lisibilité, limitez le nombre de capteurs à 3-4 maximum.</p>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-green-200 dark:border-green-800 pb-2">Étape 3: Définir la plage de dates (optionnel)</h5>
                            <p class="text-sm mb-3">Vous pouvez filtrer les données par date pour vous concentrer sur une période spécifique.</p>
                            
                            <div class="space-y-3">
                                <div>
                                    <label class="block text-sm font-medium mb-1">Date de début:</label>
                                    <input type="date" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                                </div>
                                <div>
                                    <label class="block text-sm font-medium mb-1">Date de fin:</label>
                                    <input type="date" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                                </div>
                            </div>
                            
                            <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">Laissez ces champs vides pour utiliser toutes les données disponibles.</p>
                        </div>
                        
                        <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg flex flex-col justify-between">
                            <div>
                                <h5 class="font-semibold mb-3 border-b border-green-200 dark:border-green-800 pb-2">Étape 4: Générer le graphique</h5>
                                <p class="text-sm mb-3">Cliquez sur le bouton ci-dessous pour générer le graphique avec les paramètres sélectionnés.</p>
                            </div>
                            
                            <div class="mt-4">
                                <button class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md transition-colors duration-300 transform hover:scale-[1.02]">
                                    Générer le graphique
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-green-600 dark:text-green-400 flex items-center">
                        <i class='bx bx-category-alt text-xl mr-2'></i> Types de graphiques disponibles
                    </h4>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-white dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:shadow-md">
                            <h5 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Température en fonction du temps</h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Montre l'évolution de la température au fil du temps pour chaque capteur sélectionné.</p>
                            <div class="bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
                                <p class="text-xs"><strong>Utilité:</strong> Visualiser les variations de température et comparer différents emplacements.</p>
                                <p class="text-xs mt-1"><strong>Données requises:</strong> Date, Température</p>
                            </div>
                        </div>
                        
                        <div class="bg-white dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:shadow-md">
                            <h5 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Humidité en fonction du temps</h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Montre l'évolution de l'humidité relative au fil du temps pour chaque capteur sélectionné.</p>
                            <div class="bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
                                <p class="text-xs"><strong>Utilité:</strong> Surveiller les niveaux d'humidité et identifier les périodes de risque.</p>
                                <p class="text-xs mt-1"><strong>Données requises:</strong> Date, Humidité</p>
                            </div>
                        </div>
                        
                        <div class="bg-white dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:shadow-md">
                            <h5 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Amplitude thermique quotidienne</h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Calcule et affiche la différence entre la température maximale et minimale pour chaque jour.</p>
                            <div class="bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
                                <p class="text-xs"><strong>Utilité:</strong> Évaluer la stabilité thermique et l'efficacité de l'isolation.</p>
                                <p class="text-xs mt-1"><strong>Données requises:</strong> Date, Température</p>
                            </div>
                        </div>
                        
                        <div class="bg-white dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:shadow-md">
                            <h5 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Amplitude hydrique quotidienne</h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Calcule et affiche la différence entre l'humidité maximale et minimale pour chaque jour.</p>
                            <div class="bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
                                <p class="text-xs"><strong>Utilité:</strong> Évaluer la stabilité hygrométrique et identifier les variations importantes.</p>
                                <p class="text-xs mt-1"><strong>Données requises:</strong> Date, Humidité</p>
                            </div>
                        </div>
                        
                        <div class="bg-white dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:shadow-md">
                            <h5 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Profil d'humidité par capteur</h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Affiche la distribution statistique de l'humidité pour chaque capteur sous forme de boîte à moustaches.</p>
                            <div class="bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
                                <p class="text-xs"><strong>Utilité:</strong> Comparer les profils d'humidité entre différents emplacements.</p>
                                <p class="text-xs mt-1"><strong>Données requises:</strong> Humidité</p>
                            </div>
                        </div>
                        
                        <div class="bg-white dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 transform transition-all duration-300 hover:shadow-md">
                            <h5 class="font-semibold mb-2 text-blue-600 dark:text-blue-400">Risque de point de rosée</h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Analyse et visualise le risque de condensation en comparant la température et le point de rosée.</p>
                            <div class="bg-gray-50 dark:bg-gray-800 p-2 rounded-lg">
                                <p class="text-xs"><strong>Utilité:</strong> Identifier les périodes à risque de condensation et de développement de moisissures.</p>
                                <p class="text-xs mt-1"><strong>Données requises:</strong> Date, Température, Humidité (ou Point de rosée)</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-green-600 dark:text-green-400 flex items-center">
                        <i class='bx bx-export text-xl mr-2'></i> Exporter un graphique
                    </h4>
                    
                    <p class="mb-4">Une fois le graphique généré, vous pouvez l'exporter pour l'inclure dans vos rapports ou le partager :</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
                        <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-2 flex items-center">
                                <i class='bx bx-download text-green-500 mr-2'></i> Télécharger un graphique individuel
                            </h5>
                            <p class="text-sm mb-3">Chaque graphique généré est accompagné d'un bouton de téléchargement dans le coin supérieur droit.</p>
                            <ol class="list-decimal list-inside space-y-1 text-sm ml-2">
                                <li>Survolez le graphique que vous souhaitez télécharger</li>
                                <li>Cliquez sur l'icône de téléchargement <i class='bx bx-download text-blue-500'></i></li>
                                <li>Choisissez l'emplacement où enregistrer l'image</li>
                                <li>L'image sera enregistrée au format PNG avec une haute résolution</li>
                            </ol>
                        </div>
                        
                        <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-2 flex items-center">
                                <i class='bx bx-archive text-green-500 mr-2'></i> Télécharger tous les graphiques
                            </h5>
                            <p class="text-sm mb-3">Si vous avez généré plusieurs graphiques, vous pouvez tous les télécharger en une seule fois.</p>
                            <ol class="list-decimal list-inside space-y-1 text-sm ml-2">
                                <li>Après avoir généré tous les graphiques, un bouton "Télécharger toutes les images" apparaît en bas de la page</li>
                                <li>Cliquez sur ce bouton pour télécharger toutes les images</li>
                                <li>Choisissez le dossier de destination</li>
                                <li>Les images seront enregistrées dans un dossier avec la date du jour</li>
                            </ol>
                        </div>
                    </div>
                    
                    <div class="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg border-l-4 border-blue-500">
                        <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-info-circle text-blue-500 mr-2'></i> Information</h5>
                        <p class="text-sm">Les graphiques exportés incluent automatiquement des informations sur les capteurs, la période couverte et les unités de mesure, ce qui les rend prêts à être utilisés dans des rapports professionnels.</p>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-3 text-green-600 dark:text-green-400 flex items-center">
                            <i class='bx bx-error-alt text-xl mr-2'></i> Erreurs possibles
                        </h4>
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Aucun capteur sélectionné</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Vous devez sélectionner au moins un capteur pour générer un graphique.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Cochez au moins un capteur dans la liste.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Données insuffisantes</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Le capteur ne contient pas assez de données pour générer le graphique demandé.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Vérifiez que le capteur contient suffisamment de données ou sélectionnez une plage de dates plus large.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Colonnes manquantes</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Le type de graphique sélectionné nécessite des colonnes qui n'ont pas été mappées.</p>
                                <p class="text-sm text-blue-600 dark:text-blue-400 mt-1"><strong>Solution:</strong> Retournez à la section Mappage des Colonnes pour mapper toutes les colonnes nécessaires.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-3 text-green-600 dark:text-green-400 flex items-center">
                            <i class='bx bx-bulb text-xl mr-2'></i> Astuces avancées
                        </h4>
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Comparaison de capteurs</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Pour comparer efficacement plusieurs capteurs, sélectionnez des capteurs de même type (intérieur vs extérieur).</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Analyse saisonnière</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Utilisez les filtres de date pour analyser séparément les données d'été et d'hiver afin d'identifier les différences saisonnières.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <p class="font-medium text-sm">Identification des anomalies</p>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Les pics ou chutes soudaines dans les graphiques peuvent indiquer des problèmes comme des fenêtres ouvertes ou des défaillances de chauffage.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg mb-4 border-l-4 border-green-500 animate__animated animate__pulse animate__infinite animate__slow">
                    <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-bulb text-green-500 mr-2'></i> Astuce</h5>
                    <p>Pour comparer des capteurs, sélectionnez-en plusieurs avant de générer un graphique. L'application normalisera automatiquement les données pour assurer une comparaison équitable, même si les capteurs ont des fréquences d'échantillonnage différentes.</p>
                </div>
            `
        },
        {
            id: "history",
            title: "Historique",
            icon: "bx bx-history text-amber-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-amber-50 to-yellow-50 dark:from-amber-900/30 dark:to-yellow-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">La section <strong>Historique</strong> vous permet de consulter toutes les opérations effectuées dans l'application et de suivre les modifications apportées à vos capteurs et fichiers.</p>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-amber-600 dark:text-amber-400 flex items-center">
                        <i class='bx bx-list-ul text-xl mr-2'></i> Consulter l'historique
                    </h4>
                    
                    <p class="mb-4">L'historique affiche les informations suivantes pour chaque action :</p>
                    
                    <div class="overflow-x-auto mb-6">
                        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                            <thead>
                                <tr class="bg-gray-100 dark:bg-gray-700">
                                    <th class="py-2 px-4 border-b text-left">Date et heure</th>
                                    <th class="py-2 px-4 border-b text-left">Action</th>
                                    <th class="py-2 px-4 border-b text-left">Capteur</th>
                                    <th class="py-2 px-4 border-b text-left">Détails</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">2023-06-15 14:32:45</td>
                                    <td class="py-2 px-4"><span class="px-2 py-1 bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200 rounded text-xs">Ajout capteur</span></td>
                                    <td class="py-2 px-4">Salon</td>
                                    <td class="py-2 px-4">Capteur ajouté avec succès</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">2023-06-15 14:35:12</td>
                                    <td class="py-2 px-4"><span class="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded text-xs">Association fichier</span></td>
                                    <td class="py-2 px-4">Salon</td>
                                    <td class="py-2 px-4">Fichier "donnees_salon.xlsx" associé</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">2023-06-15 14:38:27</td>
                                    <td class="py-2 px-4"><span class="px-2 py-1 bg-purple-100 dark:bg-purple-900/50 text-purple-800 dark:text-purple-200 rounded text-xs">Mappage colonnes</span></td>
                                    <td class="py-2 px-4">Salon</td>
                                    <td class="py-2 px-4">Colonnes mappées: date, température, humidité</td>
                                </tr>
                                <tr class="hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">2023-06-15 14:42:05</td>
                                    <td class="py-2 px-4"><span class="px-2 py-1 bg-yellow-100 dark:bg-yellow-900/50 text-yellow-800 dark:text-yellow-200 rounded text-xs">Génération graphique</span></td>
                                    <td class="py-2 px-4">Salon</td>
                                    <td class="py-2 px-4">Graphique "Température en fonction du temps" généré</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="bg-amber-50 dark:bg-amber-900/30 p-4 rounded-lg">
                        <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-info-circle text-amber-500 mr-2'></i> Utilité de l'historique</h5>
                        <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                            <li>Suivre les modifications apportées à vos capteurs</li>
                            <li>Vérifier quand un fichier a été associé ou modifié</li>
                            <li>Identifier les actions qui ont pu causer des problèmes</li>
                            <li>Garder une trace de toutes les opérations pour référence future</li>
                        </ul>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-amber-600 dark:text-amber-400 flex items-center">
                        <i class='bx bx-filter-alt text-xl mr-2'></i> Filtrer l'historique
                    </h4>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="bg-amber-50 dark:bg-amber-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-amber-200 dark:border-amber-800 pb-2">Filtrer par type d'action</h5>
                            <p class="text-sm mb-3">Vous pouvez filtrer l'historique pour n'afficher que certains types d'actions.</p>
                            <div class="space-y-2">
                                <div class="flex items-center">
                                    <input type="checkbox" id="filter-add" class="mr-2" checked>
                                    <label for="filter-add" class="text-sm">Ajout de capteur</label>
                                </div>
                                <div class="flex items-center">
                                    <input type="checkbox" id="filter-file" class="mr-2" checked>
                                    <label for="filter-file" class="text-sm">Association de fichier</label>
                                </div>
                                <div class="flex items-center">
                                    <input type="checkbox" id="filter-mapping" class="mr-2" checked>
                                    <label for="filter-mapping" class="text-sm">Mappage de colonnes</label>
                                </div>
                                <div class="flex items-center">
                                    <input type="checkbox" id="filter-graph" class="mr-2" checked>
                                    <label for="filter-graph" class="text-sm">Génération de graphique</label>
                                </div>
                                <div class="flex items-center">
                                    <input type="checkbox" id="filter-delete" class="mr-2" checked>
                                    <label for="filter-delete" class="text-sm">Suppression</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="bg-amber-50 dark:bg-amber-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-amber-200 dark:border-amber-800 pb-2">Filtrer par capteur</h5>
                            <p class="text-sm mb-3">Vous pouvez filtrer l'historique pour n'afficher que les actions concernant certains capteurs.</p>
                            <div class="p-2 bg-white dark:bg-gray-800 rounded border border-amber-200 dark:border-amber-800 max-h-32 overflow-y-auto">
                                <div class="flex items-center mb-2">
                                    <input type="checkbox" id="capteur-filter-1" class="mr-2" checked>
                                    <label for="capteur-filter-1" class="text-sm">Salon</label>
                                </div>
                                <div class="flex items-center mb-2">
                                    <input type="checkbox" id="capteur-filter-2" class="mr-2" checked>
                                    <label for="capteur-filter-2" class="text-sm">Chambre</label>
                                </div>
                                <div class="flex items-center">
                                    <input type="checkbox" id="capteur-filter-3" class="mr-2" checked>
                                    <label for="capteur-filter-3" class="text-sm">Extérieur</label>
                                </div>
                            </div>
                            <button class="mt-3 w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold py-1 px-3 rounded-md text-sm transition-colors duration-300">
                                Appliquer les filtres
                            </button>
                        </div>
                    </div>
                    
                    <div class="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg border-l-4 border-blue-500">
                        <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-search text-blue-500 mr-2'></i> Recherche</h5>
                        <p class="text-sm">Vous pouvez également utiliser la barre de recherche en haut de la table pour rechercher des termes spécifiques dans l'historique.</p>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-amber-600 dark:text-amber-400 flex items-center">
                        <i class='bx bx-export text-xl mr-2'></i> Exporter l'historique
                    </h4>
                    
                    <p class="mb-4">Vous pouvez exporter l'historique complet ou filtré pour le conserver ou l'analyser en dehors de l'application :</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <button class="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md flex items-center justify-center transition-colors duration-300 transform hover:scale-[1.02]">
                            <i class='bx bx-file-csv mr-2'></i> Exporter en CSV
                        </button>
                        
                        <button class="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md flex items-center justify-center transition-colors duration-300 transform hover:scale-[1.02]">
                            <i class='bx bx-file-excel mr-2'></i> Exporter en Excel
                        </button>
                        
                        <button class="bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-md flex items-center justify-center transition-colors duration-300 transform hover:scale-[1.02]">
                            <i class='bx bx-file-pdf mr-2'></i> Exporter en PDF
                        </button>
                    </div>
                    
                    <div class="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg border-l-4 border-yellow-500">
                        <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-info-circle text-yellow-500 mr-2'></i> Remarque</h5>
                        <p class="text-sm">L'export inclura uniquement les entrées actuellement affichées après application des filtres.</p>
                    </div>
                </div>
            `
        },
        {
            id: "tips",
            title: "Conseils et astuces",
            icon: "bx bx-bulb text-yellow-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-yellow-50 to-orange-50 dark:from-yellow-900/30 dark:to-orange-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">Cette section regroupe des conseils et astuces pour tirer le meilleur parti de ClimaGraph et optimiser votre analyse de données climatiques.</p>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-4 text-yellow-600 dark:text-yellow-400 flex items-center">
                            <i class='bx bx-file text-xl mr-2'></i> Formats de fichiers supportés
                        </h4>
                        
                        <div class="space-y-4">
                            <div class="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg flex items-start">
                                <i class='bx bxs-file-doc text-blue-500 text-2xl mr-3'></i>
                                <div>
                                    <h5 class="font-semibold mb-1">Excel (.xlsx, .xls)</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Feuilles de calcul Microsoft Excel. Format idéal pour les données organisées en colonnes avec en-têtes.</p>
                                    <p class="text-xs text-blue-600 dark:text-blue-400 mt-1"><strong>Conseil:</strong> Utilisez des noms de colonnes explicites comme "Date", "Température (°C)", "Humidité (%)".</p>
                                </div>
                            </div>
                            
                            <div class="p-3 bg-green-50 dark:bg-green-900/30 rounded-lg flex items-start">
                                <i class='bx bxs-file-txt text-green-500 text-2xl mr-3'></i>
                                <div>
                                    <h5 class="font-semibold mb-1">CSV (.csv)</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Fichiers de valeurs séparées par des virgules. Format simple et universel.</p>
                                    <p class="text-xs text-green-600 dark:text-green-400 mt-1"><strong>Conseil:</strong> Assurez-vous que le séparateur est bien une virgule et que la première ligne contient les en-têtes.</p>
                                </div>
                            </div>
                            
                            <div class="p-3 bg-purple-50 dark:bg-purple-900/30 rounded-lg flex items-start">
                                <i class='bx bxs-file text-purple-500 text-2xl mr-3'></i>
                                <div>
                                    <h5 class="font-semibold mb-1">HOBO (.hobo)</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Fichiers exportés depuis les enregistreurs de données HOBO. Format spécifique aux capteurs HOBO.</p>
                                    <p class="text-xs text-purple-600 dark:text-purple-400 mt-1"><strong>Conseil:</strong> Exportez directement depuis le logiciel HOBOware sans modifier la structure.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
                        <h4 class="font-semibold mb-4 text-yellow-600 dark:text-yellow-400 flex items-center">
                            <i class='bx bx-line-chart text-xl mr-2'></i> Optimisation des graphiques
                        </h4>
                        
                        <div class="space-y-4">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <h5 class="font-semibold mb-1 flex items-center">
                                    <i class='bx bx-bar-chart-alt-2 text-yellow-500 mr-2'></i> Limiter le nombre de capteurs
                                </h5>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Pour des graphiques plus lisibles, limitez le nombre de capteurs à 3-4 maximum par graphique.</p>
                                <p class="text-xs text-blue-600 dark:text-blue-400 mt-1"><strong>Pourquoi?</strong> Trop de lignes rendent le graphique difficile à interpréter et peuvent masquer des tendances importantes.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <h5 class="font-semibold mb-1 flex items-center">
                                    <i class='bx bx-calendar text-yellow-500 mr-2'></i> Utiliser la plage de dates
                                </h5>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Utilisez la plage de dates pour vous concentrer sur des périodes spécifiques (été, hiver, semaine, mois).</p>
                                <p class="text-xs text-blue-600 dark:text-blue-400 mt-1"><strong>Pourquoi?</strong> Analyser des périodes plus courtes permet de mieux visualiser les détails et les variations subtiles.</p>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                                <h5 class="font-semibold mb-1 flex items-center">
                                    <i class='bx bx-paint text-yellow-500 mr-2'></i> Distinction des capteurs
                                </h5>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Les capteurs extérieurs sont affichés avec des lignes pointillées pour les distinguer facilement des capteurs intérieurs.</p>
                                <p class="text-xs text-blue-600 dark:text-blue-400 mt-1"><strong>Astuce:</strong> Incluez toujours un capteur extérieur pour contextualiser les données intérieures.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-yellow-600 dark:text-yellow-400 flex items-center">
                        <i class='bx bx-analyse text-xl mr-2'></i> Interprétation des données
                    </h4>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div class="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-2 text-center">Amplitude thermique</h5>
                            <div class="flex justify-center mb-3">
                                <i class='bx bx-line-chart text-yellow-500 text-3xl'></i>
                            </div>
                            <p class="text-sm text-gray-600 dark:text-gray-400 text-center">Une amplitude élevée peut indiquer une mauvaise isolation ou une ventilation excessive.</p>
                            <div class="mt-2 p-2 bg-white dark:bg-gray-800 rounded text-xs">
                                <p><strong>Bonne isolation:</strong> < 5°C d'amplitude quotidienne</p>
                                <p><strong>Isolation moyenne:</strong> 5-10°C d'amplitude</p>
                                <p><strong>Mauvaise isolation:</strong> > 10°C d'amplitude</p>
                            </div>
                        </div>
                        
                        <div class="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-2 text-center">Risque de point de rosée</h5>
                            <div class="flex justify-center mb-3">
                                <i class='bx bx-droplet text-yellow-500 text-3xl'></i>
                            </div>
                            <p class="text-sm text-gray-600 dark:text-gray-400 text-center">Si la température de surface est inférieure au point de rosée, il y a risque de condensation.</p>
                            <div class="mt-2 p-2 bg-white dark:bg-gray-800 rounded text-xs">
                                <p><strong>Zone sûre:</strong> Température > Point de rosée + 3°C</p>
                                <p><strong>Zone à risque:</strong> Température entre Point de rosée et Point de rosée + 3°C</p>
                                <p><strong>Zone critique:</strong> Température ≤ Point de rosée</p>
                            </div>
                        </div>
                        
                        <div class="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg">
                            <h5 class="font-semibold mb-2 text-center">Humidité relative</h5>
                            <div class="flex justify-center mb-3">
                                <i class='bx bx-water text-yellow-500 text-3xl'></i>
                            </div>
                            <p class="text-sm text-gray-600 dark:text-gray-400 text-center">L'humidité relative idéale se situe entre 40% et 60% pour un confort optimal.</p>
                            <div class="mt-2 p-2 bg-white dark:bg-gray-800 rounded text-xs">
                                <p><strong>Trop sec:</strong> < 30% (irritations, électricité statique)</p>
                                <p><strong>Idéal:</strong> 40-60% (confort optimal)</p>
                                <p><strong>Trop humide:</strong> > 70% (risque de moisissures)</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg mb-4 border-l-4 border-purple-500">
                        <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-search-alt text-purple-500 mr-2'></i> Analyse avancée</h5>
                        <p class="text-sm">Pour une analyse plus approfondie, exportez vos graphiques et comparez les données sur différentes périodes (été/hiver, jour/nuit) pour identifier les tendances et les anomalies. Recherchez les corrélations entre les changements de température extérieure et intérieure pour évaluer l'inertie thermique du bâtiment.</p>
                    </div>
                    
                    <div class="p-4 bg-white dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
                        <h5 class="font-semibold mb-3 text-center">Exemple d'interprétation</h5>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <h6 class="font-medium text-sm mb-2">Observation</h6>
                                <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                                    <li>Température intérieure: 18-22°C</li>
                                    <li>Amplitude thermique: 4°C</li>
                                    <li>Humidité: 55-65%</li>
                                    <li>Température extérieure: 5-15°C</li>
                                </ul>
                            </div>
                            <div>
                                <h6 class="font-medium text-sm mb-2">Interprétation</h6>
                                <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                                    <li>Bonne isolation thermique (faible amplitude)</li>
                                    <li>Humidité légèrement élevée mais acceptable</li>
                                    <li>Bonne inertie thermique (faible impact des variations extérieures)</li>
                                    <li>Conditions globalement confortables</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-yellow-600 dark:text-yellow-400 flex items-center">
                        <i class='bx bx-book-open text-xl mr-2'></i> Bonnes pratiques
                    </h4>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-start">
                                <div class="bg-green-100 dark:bg-green-900/50 p-2 rounded-full mr-3">
                                    <i class='bx bx-check text-green-500 text-xl'></i>
                                </div>
                                <div>
                                    <h5 class="font-semibold mb-1">Nommez clairement vos capteurs</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Utilisez des noms descriptifs qui indiquent l'emplacement précis (ex: "Salon Nord", "Chambre Sud").</p>
                                </div>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-start">
                                <div class="bg-green-100 dark:bg-green-900/50 p-2 rounded-full mr-3">
                                    <i class='bx bx-check text-green-500 text-xl'></i>
                                </div>
                                <div>
                                    <h5 class="font-semibold mb-1">Incluez toujours un capteur extérieur</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Les données extérieures fournissent un contexte essentiel pour interpréter les variations intérieures.</p>
                                </div>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-start">
                                <div class="bg-green-100 dark:bg-green-900/50 p-2 rounded-full mr-3">
                                    <i class='bx bx-check text-green-500 text-xl'></i>
                                </div>
                                <div>
                                    <h5 class="font-semibold mb-1">Analysez des périodes spécifiques</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Concentrez-vous sur des périodes représentatives (canicule, vague de froid) pour mieux évaluer les performances.</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="space-y-3">
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-start">
                                <div class="bg-red-100 dark:bg-red-900/50 p-2 rounded-full mr-3">
                                    <i class='bx bx-x text-red-500 text-xl'></i>
                                </div>
                                <div>
                                    <h5 class="font-semibold mb-1">Évitez de placer les capteurs près des sources de chaleur</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Les radiateurs, appareils électroniques ou fenêtres ensoleillées peuvent fausser les mesures.</p>
                                </div>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-start">
                                <div class="bg-red-100 dark:bg-red-900/50 p-2 rounded-full mr-3">
                                    <i class='bx bx-x text-red-500 text-xl'></i>
                                </div>
                                <div>
                                    <h5 class="font-semibold mb-1">Ne comparez pas des périodes trop différentes</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Comparer l'été et l'hiver directement peut mener à des conclusions erronées.</p>
                                </div>
                            </div>
                            
                            <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-start">
                                <div class="bg-red-100 dark:bg-red-900/50 p-2 rounded-full mr-3">
                                    <i class='bx bx-x text-red-500 text-xl'></i>
                                </div>
                                <div>
                                    <h5 class="font-semibold mb-1">Ne négligez pas les métadonnées</h5>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Notez les événements importants (ouverture de fenêtres, changements de chauffage) qui peuvent expliquer certaines variations.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg mb-4 border-l-4 border-yellow-500 animate__animated animate__pulse animate__infinite animate__slow">
                    <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-bulb text-yellow-500 mr-2'></i> Conseil final</h5>
                    <p>Pour une analyse complète, combinez plusieurs types de graphiques. Par exemple, utilisez d'abord le graphique de température en fonction du temps pour identifier les tendances générales, puis l'amplitude thermique pour évaluer l'isolation, et enfin le risque de point de rosée pour repérer les zones problématiques.</p>
                </div>
            `
        },
        {
            id: "troubleshooting",
            title: "Dépannage",
            icon: "bx bx-wrench text-red-500",
            content: `
                <div class="p-5 bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/30 dark:to-pink-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
                    <p class="mb-4">Cette section vous aide à résoudre les problèmes courants que vous pourriez rencontrer lors de l'utilisation de ClimaGraph.</p>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                        <i class='bx bx-error-circle text-xl mr-2'></i> Problèmes courants et solutions
                    </h4>
                    
                    <div class="space-y-6">
                        <div class="p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
                            <h5 class="font-semibold mb-3 flex items-center">
                                <i class='bx bx-file text-red-500 mr-2'></i> Le fichier ne se charge pas correctement
                            </h5>
                            
                            <div class="space-y-3 ml-6">
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Le format du fichier n'est pas supporté.</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Le fichier est corrompu ou protégé par un mot de passe.</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Le fichier ne contient pas de données de date et de température.</p>
                                </div>
                            </div>
                            
                            <div class="mt-3 p-3 bg-white dark:bg-gray-800 rounded-lg">
                                <h6 class="font-semibold mb-2 text-green-600 dark:text-green-400 flex items-center">
                                    <i class='bx bx-bulb text-green-500 mr-2'></i> Solutions
                                </h6>
                                <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                                    <li>Vérifiez que le format du fichier est supporté (.xlsx, .xls, .csv, .hobo)</li>
                                    <li>Assurez-vous que le fichier n'est pas corrompu en l'ouvrant dans son application d'origine</li>
                                    <li>Vérifiez que le fichier contient bien des colonnes de date et de température</li>
                                    <li>Essayez d'exporter à nouveau le fichier depuis sa source originale</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
                            <h5 class="font-semibold mb-3 flex items-center">
                                <i class='bx bx-brain text-red-500 mr-2'></i> Le mappage automatique ne fonctionne pas
                            </h5>
                            
                            <div class="space-y-3 ml-6">
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Les noms de colonnes ne contiennent pas de mots-clés reconnaissables.</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Le fichier utilise une langue différente pour les noms de colonnes.</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Les colonnes ont des noms génériques (ex: "Colonne1", "Colonne2").</p>
                                </div>
                            </div>
                            
                            <div class="mt-3 p-3 bg-white dark:bg-gray-800 rounded-lg">
                                <h6 class="font-semibold mb-2 text-green-600 dark:text-green-400 flex items-center">
                                    <i class='bx bx-bulb text-green-500 mr-2'></i> Solutions
                                </h6>
                                <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                                    <li>Renommez les colonnes dans votre fichier source avec des noms explicites (date, température, humidité)</li>
                                    <li>Utilisez le mappage manuel en sélectionnant les colonnes appropriées dans les listes déroulantes</li>
                                    <li>Consultez l'aperçu des données pour identifier visuellement les colonnes correctes</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
                            <h5 class="font-semibold mb-3 flex items-center">
                                <i class='bx bx-line-chart text-red-500 mr-2'></i> Impossible de générer certains graphiques
                            </h5>
                            
                            <div class="space-y-3 ml-6">
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Colonnes nécessaires non mappées (humidité ou point de rosée manquants).</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Période de données insuffisante (moins de quelques jours).</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Trop de valeurs manquantes ou invalides dans les données.</p>
                                </div>
                            </div>
                            
                            <div class="mt-3 p-3 bg-white dark:bg-gray-800 rounded-lg">
                                <h6 class="font-semibold mb-2 text-green-600 dark:text-green-400 flex items-center">
                                    <i class='bx bx-bulb text-green-500 mr-2'></i> Solutions
                                </h6>
                                <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                                    <li>Vérifiez que vous avez mappé toutes les colonnes nécessaires pour le type de graphique souhaité</li>
                                    <li>Assurez-vous que vos données couvrent une période suffisante (au moins quelques jours)</li>
                                    <li>Vérifiez la qualité de vos données et nettoyez-les si nécessaire avant de les importer</li>
                                    <li>Essayez un autre type de graphique qui nécessite moins de données ou des données différentes</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
                            <h5 class="font-semibold mb-3 flex items-center">
                                <i class='bx bx-calendar text-red-500 mr-2'></i> Les dates de filtrage ne fonctionnent pas
                            </h5>
                            
                            <div class="space-y-3 ml-6">
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">La date de début est postérieure à la date de fin.</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Les dates spécifiées sont en dehors de la plage de vos données.</p>
                                </div>
                                <div class="flex items-start">
                                    <div class="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                                        <i class='bx bx-error text-red-500 text-sm'></i>
                                    </div>
                                    <p class="text-sm text-gray-600 dark:text-gray-400">Format de date incompatible entre l'interface et vos données.</p>
                                </div>
                            </div>
                            
                            <div class="mt-3 p-3 bg-white dark:bg-gray-800 rounded-lg">
                                <h6 class="font-semibold mb-2 text-green-600 dark:text-green-400 flex items-center">
                                    <i class='bx bx-bulb text-green-500 mr-2'></i> Solutions
                                </h6>
                                <ul class="list-disc list-inside space-y-1 text-sm ml-2">
                                    <li>Vérifiez que la date de début est bien antérieure à la date de fin</li>
                                    <li>Assurez-vous que les dates spécifiées sont dans la plage de vos données</li>
                                    <li>Consultez l'aperçu des données pour voir la plage de dates disponible</li>
                                    <li>Essayez d'utiliser une plage de dates plus large ou laissez les champs vides pour utiliser toutes les données</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                        <i class='bx bx-reset text-xl mr-2'></i> Réinitialisation et récupération
                    </h4>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-gray-200 dark:border-gray-600 pb-2 flex items-center">
                                <i class='bx bx-trash text-red-500 mr-2'></i> Supprimer et recréer un capteur
                            </h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Si vous rencontrez des problèmes persistants avec un capteur, vous pouvez le supprimer et le recréer :</p>
                            <ol class="list-decimal list-inside space-y-1 text-sm ml-2">
                                <li>Allez dans la section <strong>Capteurs & Fichiers</strong></li>
                                <li>Cliquez sur le bouton <strong>Supprimer</strong> à côté du capteur problématique</li>
                                <li>Confirmez la suppression</li>
                                <li>Ajoutez un nouveau capteur avec le même nom ou un nom différent</li>
                                <li>Associez à nouveau le fichier de données</li>
                                <li>Refaites le mappage des colonnes</li>
                            </ol>
                            <div class="mt-3 p-2 bg-yellow-50 dark:bg-yellow-900/30 rounded text-xs">
                                <p><strong>Attention:</strong> La suppression d'un capteur est définitive et entraîne la perte de tous les mappages associés.</p>
                            </div>
                        </div>
                        
                        <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                            <h5 class="font-semibold mb-3 border-b border-gray-200 dark:border-gray-600 pb-2 flex items-center">
                                <i class='bx bx-revision text-blue-500 mr-2'></i> Réassocier un fichier
                            </h5>
                            <p class="text-sm text-gray-600 dark:text-gray-400 mb-3">Si le fichier de données a été modifié ou corrigé, vous pouvez le réassocier au capteur :</p>
                            <ol class="list-decimal list-inside space-y-1 text-sm ml-2">
                                <li>Allez dans la section <strong>Capteurs & Fichiers</strong></li>
                                <li>Cliquez sur le bouton <strong>Associer un fichier</strong> à côté du capteur concerné</li>
                                <li>Sélectionnez le fichier corrigé ou mis à jour</li>
                                <li>Attendez que le fichier soit chargé et analysé</li>
                                <li>Vérifiez et ajustez le mappage des colonnes si nécessaire</li>
                            </ol>
                            <div class="mt-3 p-2 bg-blue-50 dark:bg-blue-900/30 rounded text-xs">
                                <p><strong>Astuce:</strong> Cette méthode est utile si vous avez corrigé des erreurs dans votre fichier de données ou si vous avez ajouté de nouvelles mesures.</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-6 p-4 bg-red-50 dark:bg-red-900/30 rounded-lg border-l-4 border-red-500">
                        <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-error-circle text-red-500 mr-2'></i> Réinitialisation complète</h5>
                        <p class="text-sm mb-3">En dernier recours, si vous rencontrez des problèmes graves et persistants, vous pouvez réinitialiser complètement l'application :</p>
                        <ol class="list-decimal list-inside space-y-1 text-sm ml-2">
                            <li>Fermez complètement l'application</li>
                            <li>Supprimez le fichier de stockage dans le dossier de données de l'application</li>
                            <li>Redémarrez l'application</li>
                        </ol>
                        <p class="text-sm mt-2"><strong>Attention:</strong> Cette action supprimera tous vos capteurs, mappages et l'historique. Assurez-vous de sauvegarder vos fichiers de données originaux.</p>
                    </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
                    <h4 class="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                        <i class='bx bx-message-alt-error text-xl mr-2'></i> Messages d'erreur courants
                    </h4>
                    
                    <div class="overflow-x-auto">
                        <table class="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                            <thead>
                                <tr class="bg-gray-100 dark:bg-gray-700">
                                    <th class="py-2 px-4 border-b text-left">Message d'erreur</th>
                                    <th class="py-2 px-4 border-b text-left">Cause probable</th>
                                    <th class="py-2 px-4 border-b text-left">Solution</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">"Format de fichier non supporté"</td>
                                    <td class="py-2 px-4">Le fichier n'est pas au format Excel, CSV ou HOBO</td>
                                    <td class="py-2 px-4">Convertissez votre fichier dans un format supporté</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">"Impossible de détecter les colonnes"</td>
                                    <td class="py-2 px-4">Structure du fichier non reconnue</td>
                                    <td class="py-2 px-4">Vérifiez que le fichier contient des en-têtes de colonnes clairs</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">"Données insuffisantes pour générer le graphique"</td>
                                    <td class="py-2 px-4">Pas assez de points de données ou période trop courte</td>
                                    <td class="py-2 px-4">Utilisez un fichier avec plus de données ou un autre type de graphique</td>
                                </tr>
                                <tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">"Erreur lors du traitement des dates"</td>
                                    <td class="py-2 px-4">Format de date non reconnu</td>
                                    <td class="py-2 px-4">Vérifiez que les dates sont dans un format standard</td>
                                </tr>
                                <tr class="hover:bg-gray-50 dark:hover:bg-gray-700">
                                    <td class="py-2 px-4">"Colonne d'humidité requise pour ce graphique"</td>
                                    <td class="py-2 px-4">Mappage de colonne manquant</td>
                                    <td class="py-2 px-4">Mappez la colonne d'humidité ou choisissez un autre type de graphique</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div class="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg mb-4 border-l-4 border-blue-500">
                    <h5 class="font-semibold mb-2 flex items-center"><i class='bx bx-support text-blue-500 mr-2'></i> Besoin d'aide supplémentaire?</h5>
                    <p>Si vous rencontrez un problème qui n'est pas couvert dans cette section, vous pouvez contacter le support technique à l'adresse <a href="mailto:support@climagraph.com" class="text-blue-600 dark:text-blue-400 hover:underline">support@climagraph.com</a> en décrivant précisément votre problème et en joignant des captures d'écran si possible.</p>
                </div>
            `
        }
    ];
    
    hideLoading();
    updateDocumentationUI();
}

// Mise à jour de l'interface de documentation
function updateDocumentationUI() {
    const documentationPage = document.getElementById('documentation-page');
    
    // Générer le contenu HTML
    let html = `
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
            <h3 class="text-lg font-semibold mb-4">📚 Documentation ClimaGraph</h3>
            <p class="mb-6">Guide complet d'utilisation de l'application ClimaGraph.</p>
            
            <div class="flex flex-col md:flex-row gap-6">
                <!-- Menu de navigation -->
                <div class="w-full md:w-1/4">
                    <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 sticky top-4">
                        <h4 class="font-semibold mb-3">Sommaire</h4>
                        <nav class="space-y-1">
    `;
    
    // Ajouter les liens de navigation
    documentationSections.forEach(section => {
        html += `
            <a href="#${section.id}" class="doc-nav-item block px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600" onclick="scrollToSection('${section.id}')">
                ${section.title}
            </a>
        `;
    });
    
    html += `
                        </nav>
                    </div>
                </div>
                
                <!-- Contenu de la documentation -->
                <div class="w-full md:w-3/4">
    `;
    
    // Ajouter les sections de contenu
    documentationSections.forEach(section => {
        html += `
            <div id="${section.id}" class="mb-8 scroll-mt-4">
                <h3 class="text-xl font-bold mb-4 pb-2 border-b border-gray-200 dark:border-gray-700">${section.title}</h3>
                ${section.content}
            </div>
        `;
    });
    
    html += `
                </div>
            </div>
        </div>
    `;
    
    // Mettre à jour le contenu de la page
    documentationPage.innerHTML = html;
    
    // Ajouter les écouteurs d'événements pour la navigation
    document.querySelectorAll('.doc-nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('href').substring(1);
            scrollToSection(sectionId);
        });
    });
}

// Fonction pour faire défiler jusqu'à une section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
        
        // Mettre à jour la classe active dans le menu
        document.querySelectorAll('.doc-nav-item').forEach(item => {
            item.classList.remove('bg-blue-100', 'dark:bg-blue-900/30', 'text-blue-700', 'dark:text-blue-300');
        });
        
        const activeItem = document.querySelector(`.doc-nav-item[href="#${sectionId}"]`);
        if (activeItem) {
            activeItem.classList.add('bg-blue-100', 'dark:bg-blue-900/30', 'text-blue-700', 'dark:text-blue-300');
        }
    }
}
