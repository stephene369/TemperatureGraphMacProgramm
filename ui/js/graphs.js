// Variables globales
let capteursPourGraphs = [];
let graphTypes = [];
let currentChart = null;
let currentGraphData = null;

// Chargement de la page des graphiques
function loadGraphsPage() {
  showLoading("Chargement des données...");

  // Charger les capteurs disponibles pour les graphiques
  pywebview.api
    .get_capteurs_for_graphs()
    .then((response) => {
      if (response.success) {
        capteursPourGraphs = response.capteurs;

        // Charger les types de graphiques
        return pywebview.api.get_graph_types();
      } else {
        throw new Error(
          response.message || "Erreur lors du chargement des capteurs"
        );
      }
    })
    .then((response) => {
      hideLoading();

      if (response.success) {
        graphTypes = response.types;
        updateGraphsUI();
      } else {
        throw new Error(
          response.message ||
            "Erreur lors du chargement des types de graphiques"
        );
      }
    })
    .catch((error) => {
      hideLoading();
      showNotification(
        error.message || "Erreur de communication avec l'API",
        "error"
      );
      console.error("API error:", error);
    });
}

// Mise à jour de l'interface des graphiques
function updateGraphsUI() {
  const graphsPage = document.getElementById("graphs-page");

  // Générer le contenu HTML
  let html = `
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6">
              <h3 class="text-lg font-semibold mb-4">📊 Graphiques</h3>
              <p class="mb-6">Générez des graphiques à partir de vos données climatiques.</p>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div class="mb-4">
                      <label for="graph-type" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Type de graphique
                      </label>
                      <select id="graph-type" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                          <option value="all" style="background-color: #4a6cf7; color: white; border: 2px solid #3451b2; font-weight: bold;">Tous les types de graphiques</option>
                          <option value="">-- Sélectionnez un type --</option>
      `;

  // Ajouter les types de graphiques
  graphTypes.forEach((type) => {
    html += `<option value="${type.id}">${type.name}</option>`;
  });

  html += `
                      </select>
                      <p id="graph-description" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                          Sélectionnez un type de graphique pour voir sa description.
                      </p>
                  </div>
                  
                  <div class="mb-4">
                      <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Capteur à inclure
                      </label>
                      <div class="max-h-40 overflow-y-auto border border-gray-300 dark:border-gray-600 rounded-md p-2 bg-white dark:bg-gray-700">
      `;

  if (capteursPourGraphs.length === 0) {
    html += `
                          <p class="text-gray-500 dark:text-gray-400 p-2">
                              Aucun capteur disponible. Veuillez d'abord ajouter des capteurs, leur associer des fichiers et mapper les colonnes.
                          </p>
                      </div>
                  </div>
              </div>
          `;
  } else {
    // Utiliser des boutons radio pour sélectionner un seul capteur à la fois
    capteursPourGraphs.forEach((capteur) => {
      html += `
        <div class="flex items-center mb-2">
          <input type="checkbox" name="capteur-selection" id="capteur-${capteur.id}" class="capteur-checkbox mr-2" value="${capteur.id}">
          <label for="capteur-${capteur.id}" class="text-gray-900 dark:text-gray-100">${capteur.nom}</label>
        </div>
      `;
    });
    
    html += `
                      </div>
                      <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                          Sélectionnez un capteur à inclure dans le graphique.
                      </p>
                  </div>
              </div>
              
              <div class="flex justify-end mb-6">
                  <button id="generate-graph-btn" class="btn-primary" onclick="generateGraph()">
                      Générer le graphique
                  </button>
              </div>
              
              <div id="graph-container" class="hidden">
                  <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-inner mb-4">
                      <h4 id="graph-title" class="text-lg font-semibold mb-4 text-center"></h4>
                      <div class="aspect-w-16 aspect-h-9">
                          <canvas id="graph-canvas"></canvas>
                      </div>
                  </div>
                  
                  <div class="flex justify-end space-x-4">
                      <button id="export-png-btn" class="btn-secondary" onclick="exportGraph('png')">
                          Exporter en PNG
                      </button>
                      <button id="export-pdf-btn" class="btn-secondary" onclick="exportGraph('pdf')">
                          Exporter en PDF
                      </button>
                  </div>
              </div>
          </div>
          
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
              <h3 class="text-lg font-semibold mb-4">💬 Remarques</h3>
              <ul class="list-disc list-inside space-y-2 ml-4 text-gray-700 dark:text-gray-300">
                  <li>Les graphiques sont générés à partir des données du capteur sélectionné.</li>
                  <li>Certains types de graphiques nécessitent des données spécifiques (température, humidité, etc.).</li>
                  <li>Vous pouvez exporter les graphiques en PNG ou PDF pour les inclure dans vos rapports.</li>
                  <li>L'option "Tous les types de graphiques" générera automatiquement tous les graphiques disponibles pour le capteur sélectionné.</li>
              </ul>
          </div>
      `;
  }

  // Mettre à jour le contenu de la page
  graphsPage.innerHTML = html;

  // Ajouter l'écouteur d'événement pour le changement de type de graphique
  const graphTypeSelect = document.getElementById("graph-type");
  if (graphTypeSelect) {
    graphTypeSelect.addEventListener("change", updateGraphDescription);

    // Appliquer un style spécial à l'option "Tous les types de graphiques"
    const allOption = graphTypeSelect.querySelector('option[value="all"]');
    if (allOption) {
      // Le style inline est déjà appliqué, mais on peut ajouter d'autres styles si nécessaire
    }
  }

  // Sélectionner le premier capteur par défaut s'il y en a
  const firstCapteurRadio = document.querySelector(".capteur-radio");
  if (firstCapteurRadio) {
    firstCapteurRadio.checked = true;
  }
}

// Fonction pour générer le graphique
function generateGraph() {
  const graphType = document.getElementById("graph-type").value;
  const selectedCapteur = document.querySelector(
    'input[name="capteur-selection"]:checked'
  );

  if (!selectedCapteur) {
    showNotification("Veuillez sélectionner un capteur", "error");
    return;
  }

  const capteurId = selectedCapteur.value;

  // Si "Tous les types de graphiques" est sélectionné
  if (graphType === "all") {
    generateAllGraphTypes(capteurId);
    return;
  }

  if (!graphType || graphType === "") {
    showNotification("Veuillez sélectionner un type de graphique", "error");
    return;
  }

  // Générer le graphique spécifique
  showLoading("Génération du graphique en cours...");

  // Appel à l'API pour générer le graphique
  window.pywebview.api
    .generate_graph(graphType, [capteurId])
    .then((response) => {
      hideLoading();
      if (response.success) {
        // Afficher le graphique
        const graphContainer = document.getElementById("graph-container");
        graphContainer.innerHTML = "";
        graphContainer.classList.remove("hidden");

        // Créer un conteneur pour ce graphique
        const singleGraphContainer = document.createElement("div");
        singleGraphContainer.className =
          "bg-white dark:bg-gray-800 p-4 rounded-lg shadow-inner mb-6 relative";

        // Ajouter le titre et un bouton de téléchargement à côté
        const titleContainer = document.createElement("div");
        titleContainer.className = "flex justify-between items-center mb-4";

        const title = document.createElement("h4");
        title.className = "text-lg font-semibold";
        title.textContent = response.data.title;

        const downloadBtn = document.createElement("button");
        downloadBtn.className =
          "text-blue-500 hover:text-blue-700 flex items-center";
        downloadBtn.innerHTML =
          '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" /></svg> Télécharger';
        downloadBtn.title = "Télécharger cette image";
        downloadBtn.onclick = () => {
          showLoading("Préparation du téléchargement...");

          // Ouvrir une boîte de dialogue pour enregistrer l'image
          window.pywebview.api
            .save_image_with_dialog(response.image, response.data.title)
            .then((saveResponse) => {
              hideLoading();
              if (saveResponse.success) {
                showNotification(`Image enregistrée avec succès`, "success");
              } else {
                showNotification(saveResponse.message, "error");
              }
            })
            .catch((error) => {
              hideLoading();
              showNotification(
                "Erreur lors du téléchargement du graphique",
                "error"
              );
              console.error(error);
            });
        };

        titleContainer.appendChild(title);
        titleContainer.appendChild(downloadBtn);
        singleGraphContainer.appendChild(titleContainer);

        // Ajouter l'image
        const img = document.createElement("img");
        img.src = `data:image/png;base64,${response.image}`;
        img.className = "w-full";
        img.alt = response.data.title;
        singleGraphContainer.appendChild(img);

        // Ajouter au conteneur principal
        graphContainer.appendChild(singleGraphContainer);

        // Faire défiler jusqu'au graphique
        graphContainer.scrollIntoView({ behavior: "smooth" });

        // Afficher également le graphique avec Chart.js si disponible
        if (response.data && response.data.type) {
          displayGraph(response.data, response.image);
        }
      } else {
        showNotification(response.message, "error");
      }
    })
    .catch((error) => {
      hideLoading();
      showNotification("Erreur lors de la génération du graphique", "error");
      console.error(error);
    });
}

// Fonction pour télécharger un seul graphique via le backend Python
function downloadSingleGraph(capteurId, graphType, imageBase64, graphName) {
  showLoading("Préparation du téléchargement...");

  // Utiliser l'image déjà générée plutôt que de la régénérer
  window.pywebview.api
    .save_image_with_dialog(imageBase64, graphName, capteurId)
    .then((response) => {
      hideLoading();
      if (response.success) {
        showNotification(`Image enregistrée avec succès`, "success");
      } else {
        showNotification(response.message, "error");
      }
    })
    .catch((error) => {
      hideLoading();
      showNotification("Erreur lors du téléchargement du graphique", "error");
      console.error(error);
    });
}

// Fonction pour télécharger toutes les images via le backend Python
function downloadAllGraphs(capteurId, graphImages) {
  if (graphImages.length === 0) {
    showNotification("Aucun graphique à télécharger", "warning");
    return;
  }

  showLoading("Préparation du téléchargement de tous les graphiques...");

  // Demander à l'utilisateur de choisir un dossier avant de télécharger
  window.pywebview.api
    .save_all_images_with_dialog(graphImages, capteurId)
    .then((response) => {
      hideLoading();
      if (response.success) {
        showNotification(`Graphiques enregistrés avec succès`, "success");
      } else {
        showNotification(response.message, "error");
      }
    })
    .catch((error) => {
      hideLoading();
      showNotification("Erreur lors du téléchargement des graphiques", "error");
      console.error(error);
    });
}

// Fonction pour générer tous les types de graphiques
function generateAllGraphTypes(capteurId) {
  showLoading("Génération de tous les graphiques en cours...");

  // Créer un conteneur pour tous les graphiques
  const graphContainer = document.getElementById("graph-container");
  graphContainer.innerHTML =
    '<h3 class="text-xl font-bold mb-4 text-center">Tous les graphiques</h3>';
  graphContainer.classList.remove("hidden");

  // Tableau pour stocker les données des graphiques générés
  const generatedGraphs = [];

  // Générer chaque type de graphique séquentiellement
  const generateNextGraph = (index) => {
    if (index >= graphTypes.length) {
      hideLoading();

      // Ajouter le bouton de téléchargement de toutes les images
      const downloadAllContainer = document.createElement("div");
      downloadAllContainer.className = "flex justify-center mt-4 mb-6";

      const downloadAllBtn = document.createElement("button");
      downloadAllBtn.className = "btn-primary flex items-center justify-center";
      downloadAllBtn.innerHTML =
        '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" /></svg> Télécharger toutes les images';
      downloadAllBtn.onclick = () =>
        downloadAllGraphs(capteurId, generatedGraphs);

      downloadAllContainer.appendChild(downloadAllBtn);
      graphContainer.appendChild(downloadAllContainer);

      return;
    }

    const graphType = graphTypes[index];

    window.pywebview.api
      .generate_graph(graphType.id, [capteurId])
      .then((response) => {
        if (response.success) {
          // Stocker les données du graphique
          generatedGraphs.push({
            id: graphType.id,
            name: graphType.name,
            image: response.image,
          });

          // Créer un conteneur pour ce graphique
          const singleGraphContainer = document.createElement("div");
          singleGraphContainer.className =
            "bg-white dark:bg-gray-800 p-4 rounded-lg shadow-inner mb-6 relative";

          // Ajouter le titre et un bouton de téléchargement à côté
          const titleContainer = document.createElement("div");
          titleContainer.className = "flex justify-between items-center mb-4";

          const title = document.createElement("h4");
          title.className = "text-lg font-semibold";
          title.textContent = graphType.name;

          const downloadBtn = document.createElement("button");
          downloadBtn.className =
            "text-blue-500 hover:text-blue-700 flex items-center";
          downloadBtn.innerHTML =
            '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" /></svg> Télécharger';
          downloadBtn.title = "Télécharger cette image";
          downloadBtn.onclick = () =>
            downloadSingleGraph(
              capteurId,
              graphType.id,
              response.image,
              graphType.name
            );

          titleContainer.appendChild(title);
          titleContainer.appendChild(downloadBtn);
          singleGraphContainer.appendChild(titleContainer);

          // Ajouter l'image
          const img = document.createElement("img");
          img.src = `data:image/png;base64,${response.image}`;
          img.className = "w-full";
          img.alt = graphType.name;
          singleGraphContainer.appendChild(img);

          // Ajouter au conteneur principal
          graphContainer.appendChild(singleGraphContainer);
        }

        // Passer au graphique suivant
        generateNextGraph(index + 1);
      })
      .catch((error) => {
        console.error(
          `Erreur lors de la génération du graphique ${graphType.id}:`,
          error
        );
        // Continuer avec le graphique suivant malgré l'erreur
        generateNextGraph(index + 1);
      });
  };

  // Commencer la génération séquentielle
  generateNextGraph(0);
}

// Mise à jour de la description du graphique
function updateGraphDescription() {
  const graphTypeSelect = document.getElementById("graph-type");
  const graphDescription = document.getElementById("graph-description");

  const selectedType = graphTypes.find(
    (type) => type.id === graphTypeSelect.value
  );

  if (selectedType) {
    graphDescription.textContent = selectedType.description;
  } else {
    graphDescription.textContent =
      "Sélectionnez un type de graphique pour voir sa description.";
  }
}

// Afficher un graphique
function displayGraph(data) {
  // Afficher le conteneur du graphique
  const graphContainer = document.getElementById("graph-container");
  graphContainer.classList.remove("hidden");

  // Mettre à jour le titre du graphique
  document.getElementById("graph-title").textContent = data.title;

  // Récupérer le canvas
  const canvas = document.getElementById("graph-canvas");
  const ctx = canvas.getContext("2d");

  // Détruire le graphique existant s'il y en a un
  if (currentChart) {
    currentChart.destroy();
  }

  // Créer la configuration du graphique
  let config = {
    type: data.type,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {},
    },
  };

  // Configurer les données en fonction du type de graphique
  if (data.type === "scatter") {
    config.data = {
      datasets: data.datasets,
    };

    // Configurer les axes pour le graphique de dispersion
    config.options.scales = {
      x: {
        title: {
          display: true,
          text: data.x_axis,
        },
      },
      y: {
        title: {
          display: true,
          text: data.y_axis,
        },
      },
    };
  } else {
    config.data = {
      labels: data.labels,
      datasets: data.datasets,
    };

    // Configurer les axes pour les autres types de graphiques
    config.options.scales = {
      x: {
        title: {
          display: true,
          text: data.x_axis,
        },
      },
      y: {
        title: {
          display: true,
          text: data.y_axis,
        },
      },
    };
  }

  // Créer le graphique
  currentChart = new Chart(ctx, config);

  // Faire défiler jusqu'au graphique
  graphContainer.scrollIntoView({ behavior: "smooth" });
}

// Exporter un graphique
function exportGraph(format) {
  if (!currentChart) {
    showNotification("Aucun graphique à exporter", "warning");
    return;
  }

  // Récupérer l'image du graphique
  const canvas = document.getElementById("graph-canvas");
  const imageData = canvas.toDataURL("image/png");

  // Demander le nom du fichier
  const title = document.getElementById("graph-title").textContent;
  const defaultFilename = title.replace(/[^a-z0-9]/gi, "_").toLowerCase();

  const content = `
        <div class="mb-4">
            <label for="export-filename" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom du fichier
            </label>
            <input type="text" id="export-filename" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100" value="${defaultFilename}">
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Le fichier sera exporté au format ${format.toUpperCase()}.
            </p>
        </div>
    `;

  const actions = [
    {
      text: "Annuler",
      class: "btn-secondary",
      onClick: hideModal,
    },
    {
      text: "Exporter",
      class: "btn-primary",
      id: "export-btn",
      onClick: () => {
        const filename =
          document.getElementById("export-filename").value.trim() ||
          defaultFilename;
        doExportGraph(imageData, filename, format);
      },
    },
  ];

  showModal(`Exporter en ${format.toUpperCase()}`, content, actions);
}

// Effectuer l'export du graphique
function doExportGraph(imageData, filename, format) {
  // Désactiver le bouton pendant le traitement
  const exportButton = document.getElementById("export-btn");
  exportButton.disabled = true;
  exportButton.textContent = "Exportation...";

  // Envoyer la demande d'export à l'API
  pywebview.api
    .export_graph(imageData, filename, format)
    .then((response) => {
      hideModal();

      if (response.success) {
        showNotification(
          `Graphique exporté avec succès en ${format.toUpperCase()}`,
          "success"
        );
      } else {
        showNotification(
          response.message ||
            `Erreur lors de l'export en ${format.toUpperCase()}`,
          "error"
        );
      }
    })
    .catch((error) => {
      hideModal();
      showNotification("Erreur de communication avec l'API", "error");
      console.error("API error:", error);
    });
}
