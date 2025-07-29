import React, { useState, useEffect } from 'react';

const DocumentationPage = () => {
  const [activeSection, setActiveSection] = useState('intro');

  const documentationSections = [
    {
      id: "intro",
      title: "Introduction",
      icon: "bx bx-info-circle text-blue-500",
      content: (
        <div>
          <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:scale-[1.01] hover:shadow-md">
            <p className="mb-4 leading-relaxed">ISCGraph est une application d'analyse de données climatiques qui vous permet de visualiser et d'analyser les données de température et d'humidité provenant de différents capteurs.</p>
            <p className="mb-4">Cette documentation vous guidera à travers les différentes fonctionnalités de l'application et vous expliquera comment les utiliser efficacement.</p>
          </div>
          
          <div className="flex justify-center my-6 animate__animated animate__pulse animate__infinite animate__slower">
            <img src="assets/img/logo.png" alt="ISCGraph Logo" className="w-32 h-32 drop-shadow-lg" />
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
            <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg border-l-4 border-green-500 transform transition-all duration-300 hover:shadow-md">
              <h4 className="font-semibold mb-2 flex items-center"><i className='bx bx-line-chart text-green-500 mr-2'></i> Visualisation</h4>
              <p className="text-sm">Créez des graphiques interactifs pour visualiser vos données climatiques.</p>
            </div>
            
            <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg border-l-4 border-purple-500 transform transition-all duration-300 hover:shadow-md">
              <h4 className="font-semibold mb-2 flex items-center"><i className='bx bx-analyse text-purple-500 mr-2'></i> Analyse</h4>
              <p className="text-sm">Analysez les tendances et identifiez les anomalies dans vos données.</p>
            </div>
            
            <div className="bg-orange-50 dark:bg-orange-900/30 p-4 rounded-lg border-l-4 border-orange-500 transform transition-all duration-300 hover:shadow-md">
              <h4 className="font-semibold mb-2 flex items-center"><i className='bx bx-export text-orange-500 mr-2'></i> Exportation</h4>
              <p className="text-sm">Exportez vos graphiques pour les inclure dans vos rapports.</p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: "getting-started",
      title: "Premiers pas",
      icon: "bx bx-walk text-green-500",
      content: (
        <div>
          <div className="p-5 bg-gradient-to-r from-green-50 to-teal-50 dark:from-green-900/30 dark:to-teal-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
            <p className="mb-4">Pour commencer à utiliser ISCGraph, suivez ces étapes simples :</p>
          </div>
          
          <div className="relative pl-8 pb-8">
            <div className="absolute left-4 top-0 h-full w-0.5 bg-blue-500"></div>
            
            <div className="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
              <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">1</div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                <h4 className="font-semibold mb-2 text-blue-600 dark:text-blue-400">Ajoutez vos capteurs</h4>
                <p className="mb-2">Commencez par ajouter vos capteurs dans la section <strong>Capteurs & Fichiers</strong>.</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Donnez un nom significatif à chaque capteur pour faciliter leur identification ultérieure.</p>
              </div>
            </div>
            
            <div className="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
              <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">2</div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                <h4 className="font-semibold mb-2 text-blue-600 dark:text-blue-400">Associez des fichiers de données</h4>
                <p className="mb-2">Associez des fichiers de données à vos capteurs en utilisant le bouton <strong>Associer un fichier</strong>.</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Formats supportés : Excel (.xlsx, .xls), CSV (.csv), HOBO (.hobo)</p>
              </div>
            </div>
            
            <div className="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
              <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">3</div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                <h4 className="font-semibold mb-2 text-blue-600 dark:text-blue-400">Mappez les colonnes</h4>
                <p className="mb-2">Définissez quelles colonnes correspondent à la date, la température, l'humidité et le point de rosée dans la section <strong>Mappage des Colonnes</strong>.</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">L'application tentera de détecter automatiquement les colonnes, mais vous pouvez les ajuster si nécessaire.</p>
              </div>
            </div>
            
            <div className="relative transform transition-all duration-300 hover:translate-x-1">
              <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-white">4</div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-md">
                <h4 className="font-semibold mb-2 text-blue-600 dark:text-blue-400">Générez des graphiques</h4>
                <p className="mb-2">Créez différents types de graphiques dans la section <strong>Graphiques</strong> pour visualiser et analyser vos données.</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Vous pouvez générer un seul type de graphique ou tous les types en une seule fois.</p>
              </div>
            </div>
          </div>
          
          <div className="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg mt-6 border-l-4 border-yellow-500">
            <h5 className="font-semibold mb-2 flex items-center"><i className='bx bx-bulb text-yellow-500 mr-2'></i> Conseil</h5>
            <p>Avant de commencer, assurez-vous que vos fichiers de données sont bien structurés et contiennent au minimum des colonnes pour la date et la température.</p>
          </div>
        </div>
      )
    },
    {
      id: "capteurs",
      title: "Capteurs & Fichiers",
      icon: "bx bx-chip text-red-500",
      content: (
        <div>
          <div className="p-5 bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/30 dark:to-pink-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
            <p className="mb-4">La section <strong>Capteurs & Fichiers</strong> vous permet de gérer vos capteurs et les fichiers de données associés.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
              <h4 className="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                <i className='bx bx-plus-circle text-xl mr-2'></i> Ajouter un capteur
              </h4>
              <ol className="list-decimal list-inside space-y-3 ml-4 mb-4">
                <li className="pb-2 border-b border-gray-100 dark:border-gray-700">Cliquez sur le bouton <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded font-mono text-sm">Ajouter un capteur</span></li>
                <li className="pb-2 border-b border-gray-100 dark:border-gray-700">Saisissez un nom pour votre capteur (ex: "Salon", "Chambre", "Extérieur")</li>
                <li>Cliquez sur <span className="px-2 py-1 bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200 rounded font-mono text-sm">Ajouter</span> pour confirmer</li>
              </ol>
              
              <div className="bg-blue-50 dark:bg-blue-900/30 p-3 rounded-lg">
                <h5 className="font-semibold mb-1 text-sm flex items-center"><i className='bx bx-info-circle text-blue-500 mr-1'></i> Bonnes pratiques</h5>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300">
                  <li>Utilisez des noms descriptifs (ex: "Salon Nord", "Chambre Sud")</li>
                  <li>Pour les capteurs extérieurs, incluez "Ext" dans le nom pour qu'ils soient affichés avec des lignes pointillées dans les graphiques</li>
                </ul>
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md transform transition-all duration-300 hover:shadow-lg">
              <h4 className="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
                <i className='bx bx-link text-xl mr-2'></i> Associer un fichier
              </h4>
              <ol className="list-decimal list-inside space-y-3 ml-4 mb-4">
                <li className="pb-2 border-b border-gray-100 dark:border-gray-700">Cliquez sur le bouton <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded font-mono text-sm">Associer un fichier</span> à côté du capteur concerné</li>
                <li className="pb-2 border-b border-gray-100 dark:border-gray-700">Sélectionnez le fichier de données dans l'explorateur de fichiers</li>
                <li>Attendez que le fichier soit chargé et analysé (une notification de succès s'affichera)</li>
              </ol>
              
              <div className="bg-green-50 dark:bg-green-900/30 p-3 rounded-lg">
                <h5 className="font-semibold mb-1 text-sm flex items-center"><i className='bx bx-check-circle text-green-500 mr-1'></i> Formats supportés</h5>
                <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-300">
                  <li><strong>Excel</strong> (.xlsx, .xls) - Feuilles de calcul Microsoft Excel</li>
                  <li><strong>CSV</strong> (.csv) - Fichiers de valeurs séparées par des virgules</li>
                  <li><strong>HOBO</strong> (.hobo) - Fichiers exportés depuis les enregistreurs HOBO</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
            <h4 className="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
              <i className='bx bx-trash text-xl mr-2'></i> Supprimer un capteur
            </h4>
            <ol className="list-decimal list-inside space-y-3 ml-4 mb-4">
              <li className="pb-2 border-b border-gray-100 dark:border-gray-700">Cliquez sur le bouton <span className="px-2 py-1 bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200 rounded font-mono text-sm">Supprimer</span> à côté du capteur concerné</li>
              <li>Confirmez la suppression dans la boîte de dialogue qui apparaît</li>
            </ol>
            
            <div className="bg-red-50 dark:bg-red-900/30 p-3 rounded-lg border-l-4 border-red-500 animate__animated animate__headShake">
              <h5 className="font-semibold mb-1 flex items-center"><i className='bx bx-error-circle text-red-500 mr-1'></i> Attention</h5>
              <p className="text-sm text-gray-700 dark:text-gray-300">La suppression d'un capteur est <strong>définitive</strong> et entraîne également la suppression de tous les fichiers et mappages associés. Cette action ne peut pas être annulée.</p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: "mapping",
      title: "Mappage des Colonnes",
      icon: "bx bx-link-alt text-purple-500",
      content: (
        <div>
          <div className="p-5 bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/30 dark:to-indigo-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
            <p className="mb-4">La section <strong>Mappage des Colonnes</strong> vous permet de définir quelles colonnes de vos fichiers correspondent à la date, la température, l'humidité et le point de rosée.</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
            <h4 className="font-semibold mb-4 text-purple-600 dark:text-purple-400 flex items-center">
              <i className='bx bx-map-alt text-xl mr-2'></i> Mapper les colonnes
            </h4>
            
            <div className="relative pl-8 pb-8">
              <div className="absolute left-4 top-0 h-full w-0.5 bg-purple-500"></div>
              
              <div className="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">1</div>
                <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                  <h5 className="font-semibold mb-2">Sélectionner un capteur</h5>
                  <p className="text-sm">Choisissez un capteur dans la liste déroulante. Seuls les capteurs avec des fichiers associés sont affichés.</p>
                </div>
              </div>
              
              <div className="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">2</div>
                <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                  <h5 className="font-semibold mb-2">Vérifier la détection automatique</h5>
                  <p className="text-sm">L'application tente de détecter automatiquement les colonnes appropriées. Vérifiez si les sélections sont correctes.</p>
                </div>
              </div>
              
              <div className="relative mb-8 transform transition-all duration-300 hover:translate-x-1">
                <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">3</div>
                <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                  <h5 className="font-semibold mb-2">Ajuster les mappages si nécessaire</h5>
                  <p className="text-sm">Si la détection automatique n'est pas correcte, sélectionnez manuellement les colonnes appropriées :</p>
                  <ul className="list-disc list-inside space-y-2 ml-4 mt-2 text-sm">
                    <li><strong>Colonne de date</strong> : colonne contenant les dates/heures des mesures <span className="text-red-500">(obligatoire)</span></li>
                    <li><strong>Colonne de température</strong> : colonne contenant les valeurs de température <span className="text-red-500">(obligatoire)</span></li>
                    <li><strong>Colonne d'humidité</strong> : colonne contenant les valeurs d'humidité <span className="text-gray-500">(optionnelle)</span></li>
                    <li><strong>Colonne de point de rosée</strong> : colonne contenant les valeurs de point de rosée <span className="text-gray-500">(optionnelle)</span></li>
                  </ul>
                </div>
              </div>
              
              <div className="relative transform transition-all duration-300 hover:translate-x-1">
                <div className="absolute left-[-30px] top-0 flex h-8 w-8 items-center justify-center rounded-full bg-purple-500 text-white">4</div>
                <div className="bg-purple-50 dark:bg-purple-900/30 p-4 rounded-lg">
                  <h5 className="font-semibold mb-2">Enregistrer le mappage</h5>
                  <p className="text-sm">Cliquez sur le bouton <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded font-mono text-sm">Enregistrer le mappage</span> pour confirmer vos sélections.</p>
                  <p className="text-sm mt-2">Une notification de succès s'affichera si le mappage a été enregistré correctement.</p>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg mb-4 border-l-4 border-blue-500 animate__animated animate__pulse animate__infinite animate__slow">
            <h5 className="font-semibold mb-2 flex items-center"><i className='bx bx-info-circle text-blue-500 mr-2'></i> Information importante</h5>
            <p>Les colonnes de date et de température sont <strong>obligatoires</strong> pour générer des graphiques. Les colonnes d'humidité et de point de rosée sont optionnelles, mais nécessaires pour certains types de graphiques comme l'amplitude hydrique ou le risque de point de rosée.</p>
          </div>
        </div>
      )
    },
    {
      id: "graphs",
      title: "Graphiques",
      icon: "bx bx-line-chart text-green-500",
      content: (
        <div>
          <div className="p-5 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
            <p className="mb-4">La section <strong>Graphiques</strong> vous permet de générer différents types de visualisations à partir de vos données climatiques.</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
            <h4 className="font-semibold mb-4 text-green-600 dark:text-green-400 flex items-center">
              <i className='bx bx-bar-chart-alt-2 text-xl mr-2'></i> Générer un graphique
            </h4>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                <h5 className="font-semibold mb-3 border-b border-green-200 dark:border-green-800 pb-2">Étape 1: Sélectionner un type de graphique</h5>
                <p className="text-sm mb-3">Choisissez le type de graphique que vous souhaitez générer dans la liste déroulante.</p>
                <div className="p-2 bg-white dark:bg-gray-800 rounded border border-green-200 dark:border-green-800">
                  <select className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                    <option value="all">Tous les types de graphiques</option>
                    <option value="temperature_time">Température en fonction du temps</option>
                    <option value="humidity_time">Humidité en fonction du temps</option>
                    <option value="temperature_amplitude">Amplitude thermique quotidienne</option>
                    <option value="humidity_amplitude">Amplitude hydrique quotidienne</option>
                    <option value="humidity_profile">Profil d'humidité par capteur</option>
                    <option value="dew_point_risk">Risque de point de rosée</option>
                  </select>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">L'option "Tous les types de graphiques" générera automatiquement tous les graphiques disponibles.</p>
              </div>
              
              <div className="bg-green-50 dark:bg-green-900/30 p-4 rounded-lg">
                <h5 className="font-semibold mb-3 border-b border-green-200 dark:border-green-800 pb-2">Étape 2: Sélectionner les capteurs</h5>
                <p className="text-sm mb-3">Cochez un ou plusieurs capteurs à inclure dans le graphique.</p>
                <div className="p-2 bg-white dark:bg-gray-800 rounded border border-green-200 dark:border-green-800 max-h-32 overflow-y-auto">
                  <div className="flex items-center mb-2">
                    <input type="checkbox" id="capteur-1" className="mr-2" />
                    <label htmlFor="capteur-1">Salon</label>
                  </div>
                  <div className="flex items-center mb-2">
                    <input type="checkbox" id="capteur-2" className="mr-2" />
                    <label htmlFor="capteur-2">Chambre</label>
                  </div>
                  <div className="flex items-center">
                    <input type="checkbox" id="capteur-3" className="mr-2" />
                    <label htmlFor="capteur-3">Extérieur</label>
                  </div>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Pour une meilleure lisibilité, limitez le nombre de capteurs à 3-4 maximum.</p>
              </div>
            </div>
          </div>
          
          <div className="bg-yellow-50 dark:bg-yellow-900/30 p-4 rounded-lg mb-4 border-l-4 border-yellow-500 animate__animated animate__pulse animate__infinite animate__slow">
            <h5 className="font-semibold mb-2 flex items-center"><i className='bx bx-bulb text-yellow-500 mr-2'></i> Conseil final</h5>
            <p>Pour une analyse complète, combinez plusieurs types de graphiques. Par exemple, utilisez d'abord le graphique de température en fonction du temps pour identifier les tendances générales, puis l'amplitude thermique pour évaluer l'isolation, et enfin le risque de point de rosée pour repérer les zones problématiques.</p>
          </div>
        </div>
      )
    },
    {
      id: "troubleshooting",
      title: "Dépannage",
      icon: "bx bx-wrench text-red-500",
      content: (
        <div>
          <div className="p-5 bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/30 dark:to-pink-900/30 rounded-lg mb-6 transform transition-all duration-300 hover:shadow-md">
            <p className="mb-4">Cette section vous aide à résoudre les problèmes courants que vous pourriez rencontrer lors de l'utilisation de ISCGraph.</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
            <h4 className="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
              <i className='bx bx-error-circle text-xl mr-2'></i> Problèmes courants et solutions
            </h4>
            
            <div className="space-y-6">
              <div className="p-4 bg-red-50 dark:bg-red-900/30 rounded-lg">
                <h5 className="font-semibold mb-3 flex items-center">
                  <i className='bx bx-file text-red-500 mr-2'></i> Le fichier ne se charge pas correctement
                </h5>
                
                <div className="space-y-3 ml-6">
                  <div className="flex items-start">
                    <div className="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                      <i className='bx bx-error text-red-500 text-sm'></i>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Le format du fichier n'est pas supporté.</p>
                  </div>
                  <div className="flex items-start">
                    <div className="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                      <i className='bx bx-error text-red-500 text-sm'></i>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Le fichier est corrompu ou protégé par un mot de passe.</p>
                  </div>
                  <div className="flex items-start">
                    <div className="bg-white dark:bg-gray-800 p-1 rounded-full mr-2 mt-1">
                      <i className='bx bx-error text-red-500 text-sm'></i>
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Le fichier ne contient pas de données de date et de température.</p>
                  </div>
                </div>
                
                <div className="mt-3 p-3 bg-white dark:bg-gray-800 rounded-lg">
                  <h6 className="font-semibold mb-2 text-green-600 dark:text-green-400 flex items-center">
                    <i className='bx bx-bulb text-green-500 mr-2'></i> Solutions
                  </h6>
                  <ul className="list-disc list-inside space-y-1 text-sm ml-2">
                    <li>Vérifiez que le format du fichier est supporté (.xlsx, .xls, .csv, .hobo)</li>
                    <li>Assurez-vous que le fichier n'est pas corrompu en l'ouvrant dans son application d'origine</li>
                    <li>Vérifiez que le fichier contient bien des colonnes de date et de température</li>
                    <li>Essayez d'exporter à nouveau le fichier depuis sa source originale</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-5 rounded-lg shadow-md mb-6 transform transition-all duration-300 hover:shadow-lg">
            <h4 className="font-semibold mb-4 text-red-600 dark:text-red-400 flex items-center">
              <i className='bx bx-message-alt-error text-xl mr-2'></i> Messages d'erreur courants
            </h4>
            
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700">
                <thead>
                  <tr className="bg-gray-100 dark:bg-gray-700">
                    <th className="py-2 px-4 border-b text-left">Message d'erreur</th>
                    <th className="py-2 px-4 border-b text-left">Cause probable</th>
                    <th className="py-2 px-4 border-b text-left">Solution</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-2 px-4">"Format de fichier non supporté"</td>
                    <td className="py-2 px-4">Le fichier n'est pas au format Excel, CSV ou HOBO</td>
                    <td className="py-2 px-4">Convertissez votre fichier dans un format supporté</td>
                  </tr>
                  <tr className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-2 px-4">"Impossible de détecter les colonnes"</td>
                    <td className="py-2 px-4">Structure du fichier non reconnue</td>
                    <td className="py-2 px-4">Vérifiez que le fichier contient des en-têtes de colonnes clairs</td>
                  </tr>
                  <tr className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-2 px-4">"Données insuffisantes pour générer le graphique"</td>
                    <td className="py-2 px-4">Pas assez de points de données ou période trop courte</td>
                    <td className="py-2 px-4">Utilisez un fichier avec plus de données ou un autre type de graphique</td>
                  </tr>
                  <tr className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-2 px-4">"Erreur lors du traitement des dates"</td>
                    <td className="py-2 px-4">Format de date non reconnu</td>
                    <td className="py-2 px-4">Vérifiez que les dates sont dans un format standard</td>
                  </tr>
                  <tr className="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="py-2 px-4">"Colonne d'humidité requise pour ce graphique"</td>
                    <td className="py-2 px-4">Mappage de colonne manquant</td>
                    <td className="py-2 px-4">Mappez la colonne d'humidité ou choisissez un autre type de graphique</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div className="bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg mb-4 border-l-4 border-blue-500">
            <h5 className="font-semibold mb-2 flex items-center"><i className='bx bx-support text-blue-500 mr-2'></i> Besoin d'aide supplémentaire?</h5>
            <p>Si vous rencontrez un problème qui n'est pas couvert dans cette section, vous pouvez contacter le développeur à l'adresse <a href="mailto:stephenew36@gmail.com" className="text-blue-600 dark:text-blue-400 hover:underline">stephenew36@gmail.com</a> en décrivant précisément votre problème et en joignant des captures d'écran si possible.</p>
          </div>
        </div>
      )
    }
  ];

  const scrollToSection = (sectionId) => {
    setActiveSection(sectionId);
    
    // Scroll to section
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    // Handle scroll events to update active section
    const handleScroll = () => {
      const sections = documentationSections.map(s => document.getElementById(s.id)).filter(Boolean);
      
      for (let i = sections.length - 1; i >= 0; i--) {
        const section = sections[i];
        const rect = section.getBoundingClientRect();
        
        if (rect.top <= 100) {
          setActiveSection(section.id);
          break;
        }
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [documentationSections]);

  return (
    <div>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">📚 Documentation ISCGraph</h3>
        <p className="mb-6">Guide complet d'utilisation de l'application ISCGraph.</p>
        
        <div className="flex flex-col md:flex-row gap-6">
          {/* Menu de navigation */}
          <div className="w-full md:w-1/4">
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 sticky top-4">
              <h4 className="font-semibold mb-3">Sommaire</h4>
              <nav className="space-y-1">
                {documentationSections.map(section => (
                  <button
                    key={section.id}
                    onClick={() => scrollToSection(section.id)}
                    className={`doc-nav-item block w-full text-left px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors ${
                      activeSection === section.id 
                        ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' 
                        : ''
                    }`}
                  >
                    {section.title}
                  </button>
                ))}
              </nav>
            </div>
          </div>
          
          {/* Contenu de la documentation */}
          <div className="w-full md:w-3/4">
            {documentationSections.map(section => (
              <div key={section.id} id={section.id} className="mb-8 scroll-mt-4">
                <h3 className="text-xl font-bold mb-4 pb-2 border-b border-gray-200 dark:border-gray-700">
                  {section.title}
                </h3>
                {section.content}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentationPage;
