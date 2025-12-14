/**
 * Service pour communiquer avec l'API Python via pywebview
 */
export class ApiService {
  static isInitialized = false;

  static init() {
    if (this.isInitialized) return;
    
    // Vérifier si pywebview est disponible
    if (typeof window.pywebview === 'undefined' || !window.pywebview.api) {
      console.warn('pywebview not available, using mock API');
      this.setupMockAPI();
    } else {
      console.log('✅ pywebview API détectée et disponible');
    }
    
    this.isInitialized = true;
  }

  static setupMockAPI() {
    // Mock API pour le développement
    window.pywebview = {
      api: {
        get_capteurs: () => Promise.resolve({
          success: true,
          capteurs: []
        }),
        get_available_capteurs_for_statistics: () => Promise.resolve({
          success: true,
          capteurs: []
        }),
        get_data_statistics: () => Promise.resolve({
          success: false,
          message: 'API non disponible en mode développement'
        }),
        export_statistics_to_excel: () => Promise.resolve({
          success: false,
          message: 'API non disponible en mode développement'
        }),
        add_capteur: (nom) => Promise.resolve({
          success: true,
          message: `Capteur "${nom}" ajouté avec succès`,
          capteur: { id: Date.now(), nom, file_path: null, columns: null }
        }),
        delete_capteur: (id) => Promise.resolve({
          success: true,
          message: 'Capteur supprimé avec succès'
        }),
        select_file: (capteurId) => Promise.resolve({
          success: true,
          message: 'Fichier associé avec succès',
          file_path: '/mock/path/to/file.xlsx'
        }),
        get_file_columns: (capteurId) => Promise.resolve({
          success: true,
          columns: ['Date', 'Temperature', 'Humidity', 'Pressure']
        }),
        save_mapping: (capteurId, mapping) => Promise.resolve({
          success: true,
          message: 'Mappage sauvegardé avec succès'
        }),
        generate_graphs: (options) => Promise.resolve({
          success: true,
          message: 'Graphiques générés avec succès',
          files: ['graph1.png', 'graph2.png']
        }),
        get_history: () => Promise.resolve({
          success: true,
          history: []
        }),
        get_app_info: () => Promise.resolve({
          success: true,
          name: 'ISCGraph',
          version: '1.0.0'
        }),
        get_capteurs_for_graphs: () => Promise.resolve({
          success: true,
          capteurs: []
        }),
        get_graph_types: () => Promise.resolve({
          success: true,
          types: [
            { id: 'temperature', name: 'Graphique de température', description: 'Évolution de la température dans le temps' },
            { id: 'humidity', name: 'Graphique d\'humidité', description: 'Évolution de l\'humidité relative dans le temps' },
            { id: 'thermal_amplitude', name: 'Amplitude thermique', description: 'Différence entre température max et min par jour' }
          ]
        }),
        generate_graph: (graphType, capteurIds, options) => Promise.resolve({
          success: true,
          data: { title: 'Graphique test' },
          image: 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
        }),
        save_image_with_dialog: (imageData, filename) => Promise.resolve({
          success: true,
          message: 'Image sauvegardée'
        }),
        save_all_images_with_dialog: (images) => Promise.resolve({
          success: true,
          message: 'Images sauvegardées'
        }),
        get_capteurs_for_mapping: () => Promise.resolve({
          success: true,
          capteurs: [
            { id: 1, nom: 'Capteur Bureau', file_path: '/path/to/file.xlsx', columns: { date: 'Date', temperature: 'Temperature' } },
            { id: 2, nom: 'Capteur Entrepôt', file_path: '/path/to/file2.xlsx', columns: null }
          ]
        }),
        get_columns_for_mapping: (capteurId) => Promise.resolve({
          success: true,
          columns: ['Date', 'Time', 'Temperature', 'Humidity', 'Dew Point', 'Pressure']
        }),
        get_data_preview: (capteurId) => Promise.resolve({
          success: true,
          preview: {
            columns: ['Date', 'Time', 'Temperature', 'Humidity'],
            data: [
              ['2024-01-01', '10:00', '22.5', '45.2'],
              ['2024-01-01', '10:15', '22.8', '44.8'],
              ['2024-01-01', '10:30', '23.1', '44.5'],
              ['2024-01-01', '10:45', '23.3', '44.1'],
              ['2024-01-01', '11:00', '23.6', '43.8']
            ]
          }
        }),
        save_column_mapping: (capteurId, mapping) => Promise.resolve({
          success: true,
          message: 'Mappage des colonnes enregistré avec succès'
        })
      }
    };
  }

  // Méthodes pour les capteurs
  static async getCapteurs() {
    try {
      return await window.pywebview.api.get_capteurs();
    } catch (error) {
      console.error('Error getting capteurs:', error);
      return { success: false, message: 'Erreur de communication avec l\'API' };
    }
  }

  static async addCapteur(nom) {
    try {
      return await window.pywebview.api.add_capteur(nom);
    } catch (error) {
      console.error('Error adding capteur:', error);
      return { success: false, message: 'Erreur lors de l\'ajout du capteur' };
    }
  }

  static async editCapteur(id, nom) {
    try {
      return await window.pywebview.api.update_capteur(id, nom);
    } catch (error) {
      console.error('Error editing capteur:', error);
      return { success: false, message: 'Erreur lors de la modification du capteur' };
    }
  }

  static async deleteCapteur(id) {
    try {
      return await window.pywebview.api.delete_capteur(id);
    } catch (error) {
      console.error('Error deleting capteur:', error);
      return { success: false, message: 'Erreur lors de la suppression du capteur' };
    }
  }

  static async selectFile(capteurId) {
    try {
      return await window.pywebview.api.select_file(capteurId);
    } catch (error) {
      console.error('Error selecting file:', error);
      return { success: false, message: 'Erreur lors de la sélection du fichier' };
    }
  }

  // Méthodes pour le mappage
  static async getCapteursForMapping() {
    try {
      return await window.pywebview.api.get_capteurs_for_mapping();
    } catch (error) {
      console.error('Error getting capteurs for mapping:', error);
      return { success: false, message: 'Erreur lors de la récupération des capteurs pour mappage' };
    }
  }

  static async getFileColumns(capteurId) {
    try {
      return await window.pywebview.api.get_file_columns(capteurId);
    } catch (error) {
      console.error('Error getting file columns:', error);
      return { success: false, message: 'Erreur lors de la lecture des colonnes' };
    }
  }

  static async saveMapping(capteurId, mapping) {
    try {
      return await window.pywebview.api.save_mapping(capteurId, mapping);
    } catch (error) {
      console.error('Error saving mapping:', error);
      return { success: false, message: 'Erreur lors de la sauvegarde du mappage' };
    }
  }

  static async previewData(capteurId, nbLignes = 10) {
    try {
      return await window.pywebview.api.preview_data(capteurId, nbLignes);
    } catch (error) {
      console.error('Error previewing data:', error);
      return { success: false, message: 'Erreur lors de l\'aperçu des données' };
    }
  }

  // Méthodes pour les graphiques
  static async generateGraphs(options) {
    try {
      return await window.pywebview.api.generate_graphs(options);
    } catch (error) {
      console.error('Error generating graphs:', error);
      return { success: false, message: 'Erreur lors de la génération des graphiques' };
    }
  }

  static async getGraphTypes() {
    try {
      return await window.pywebview.api.get_graph_types();
    } catch (error) {
      console.error('Error getting graph types:', error);
      return { success: false, message: 'Erreur lors de la récupération des types de graphiques' };
    }
  }

  static async getCapteursForGraphs() {
    try {
      return await window.pywebview.api.get_capteurs_for_graphs();
    } catch (error) {
      console.error('Error getting capteurs for graphs:', error);
      return { success: false, message: 'Erreur lors de la récupération des capteurs pour graphiques' };
    }
  }

  static async generateGraph(graphType, capteurIds, options = {}) {
    try {
      return await window.pywebview.api.generate_graph(graphType, capteurIds, options);
    } catch (error) {
      console.error('Error generating graph:', error);
      return { success: false, message: 'Erreur lors de la génération du graphique' };
    }
  }

  static async saveImageWithDialog(imageData, filename) {
    try {
      return await window.pywebview.api.save_image_with_dialog(imageData, filename);
    } catch (error) {
      console.error('Error saving image:', error);
      return { success: false, message: 'Erreur lors de la sauvegarde de l\'image' };
    }
  }

  static async saveAllImagesWithDialog(images) {
    try {
      return await window.pywebview.api.save_all_images_with_dialog(images);
    } catch (error) {
      console.error('Error saving all images:', error);
      return { success: false, message: 'Erreur lors de la sauvegarde des images' };
    }
  }

  // Méthodes pour l'historique
  static async getHistory() {
    try {
      return await window.pywebview.api.get_history();
    } catch (error) {
      console.error('Error getting history:', error);
      return { success: false, message: 'Erreur lors de la récupération de l\'historique' };
    }
  }

  static async exportHistory() {
    try {
      return await window.pywebview.api.export_history();
    } catch (error) {
      console.error('Error exporting history:', error);
      return { success: false, message: 'Erreur lors de l\'export de l\'historique' };
    }
  }

  // Méthodes pour le mappage avancé

  static async getColumnsForMapping(capteurId) {
    try {
      return await window.pywebview.api.get_columns_for_mapping(capteurId);
    } catch (error) {
      console.error('Error getting columns for mapping:', error);
      return { success: false, message: 'Erreur lors du chargement des colonnes' };
    }
  }

  static async getDataPreview(capteurId) {
    try {
      return await window.pywebview.api.get_data_preview(capteurId);
    } catch (error) {
      console.error('Error getting data preview:', error);
      return { success: false, message: 'Erreur lors du chargement de l\'aperçu' };
    }
  }

  static async saveColumnMapping(capteurId, mapping) {
    try {
      return await window.pywebview.api.save_column_mapping(capteurId, mapping);
    } catch (error) {
      console.error('Error saving column mapping:', error);
      return { success: false, message: 'Erreur lors de l\'enregistrement du mappage' };
    }
  }

  // Méthodes pour les statistiques
  static async getDataStatistics(capteurIds, startDate = null, endDate = null) {
    try {
      return await window.pywebview.api.get_data_statistics(capteurIds, startDate, endDate);
    } catch (error) {
      console.error('Error getting data statistics:', error);
      return { success: false, message: 'Erreur lors du calcul des statistiques' };
    }
  }

  static async getAvailableCapteursForStatistics() {
    try {
      return await window.pywebview.api.get_available_capteurs_for_statistics();
    } catch (error) {
      console.error('Error getting available capteurs for statistics:', error);
      return { success: false, message: 'Erreur lors de la récupération des capteurs disponibles' };
    }
  }

  static async exportStatisticsToExcel(capteurIds, startDate = null, endDate = null , filetype='excel') {
    try {
      return await window.pywebview.api.export_statistics_to_excel(capteurIds, startDate, endDate,filetype);
    } catch (error) {
      console.error('Error exporting statistics to Excel:', error);
      return { success: false, message: 'Erreur lors de l\'export des statistiques' };
    }
  }

  // Méthodes utilitaires
  static async getAppInfo() {
    try {
      return await window.pywebview.api.get_app_info();
    } catch (error) {
      console.error('Error getting app info:', error);
      return { success: false, message: 'Erreur lors de la récupération des informations de l\'application' };
    }
  }
}
