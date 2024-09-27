<template>
    <v-container style="max-width: 1200px">
        <v-row>
            <!-- Liste des logements à gauche -->
            <v-col cols="12" md="12" class="logements-list">
                <h2>Liste des Logements</h2>
                <v-data-table :headers="colonnes" :items="logements">
                    <template v-slot:[`item.action`]="{ item }">
                        <v-icon style="color:darkorange" small @click="modifierLogement(item)">mdi-pencil</v-icon>
                        <v-icon style="color: darkred" small @click="supprimerLogement(item.id)">mdi-delete</v-icon>
                    </template>
                </v-data-table>
            </v-col>

            <v-col cols="12" md="12" class="logements-list">
                <h2>{{ indexEdition === -1 ? 'Ajouter ou Modifier un Logement' : 'Modifier le Logement' }}</h2>
                <v-form @submit.prevent="ajouterLogement">
                    <v-text-field v-model="nouveauLogement.nbChambres" :rules="reglesChambres" label="Nombre de chambres" required></v-text-field>
                    <v-text-field v-model="nouveauLogement.superficie" :rules="reglesSuperficie" label="Superficie" required></v-text-field>
                    <v-text-field v-model="nouveauLogement.nbFenetre" :rules="reglesFenetre" label="Nombre de fenêtres" required></v-text-field>
                    <v-text-field v-model="nouveauLogement.prix" :rules="reglesPrix" label="Prix" required></v-text-field>
                    <v-date-picker v-model="nouveauLogement.annee" :rules="reglesAnnee" label="Année" required></v-date-picker>
                    <v-select
                            class="mt-2"
                            v-model="nouveauLogement.ville"
                            :items="villesDisponibles"
                            label="Ville"
                            required
                    ></v-select>
                    <v-checkbox v-model="nouveauLogement.balcon" label="Balcon"></v-checkbox>
                    <v-checkbox v-model="nouveauLogement.garage" label="Garage"></v-checkbox>
                    <v-row>
                        <v-col cols="12" class="d-flex align-center">
                            <label>Note</label>
                            <v-rating v-model="nouveauLogement.note" :rules="reglesNote" required></v-rating>
                        </v-col>
                    </v-row>
                    <v-select v-model="nouveauLogement.categoriePrix" :items="categoriesPrix" label="Catégorie de prix" required></v-select>
                    <v-btn color="success" dark type="submit">{{ indexEdition === -1 ? 'Ajouter et Sauvegarder' : 'Modifier et Sauvegarder' }}</v-btn>
                </v-form>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    name: 'LogementListe',
    data() {
        return {
            logements: [],
            nouveauLogement: { nbChambres: '', superficie: '', nbFenetre: '', prix: '', annee: null, balcon: false, garage: false, note: 0, categoriePrix: '', ville: '' },
            indexEdition: -1,
            colonnes: [
                { title: 'ID', value: 'id' },
                { title: 'Chambres', value: 'nbChambres' },
                { title: 'Superficie', value: 'superficie' },
                { title: 'Fenêtres', value: 'nbFenetre' },
                { title: 'Prix', value: 'prix' },
                { title: 'Année', value: 'annee' },
                { title: 'Balcon', value: 'balcon' },
                { title: 'Garage', value: 'garage' },
                { title: 'Note', value: 'note' },
                { title: 'Catégorie de prix', value: 'categoriePrix' },
                { title: 'Ville', value: 'ville' },
                { title: 'Actions', value: 'action', sortable: false },
            ],
            reglesChambres: [
                v => (!v || v.length === 0 || (v >= 1 && v <= 100)) || 'Le nombre de chambres doit être entre 1 et 100'
            ],
            reglesSuperficie: [
                v => (!v || v.length === 0 || (v >= 5 && v <= 600)) || 'La superficie doit être entre 5 et 600 m²'
            ],
            reglesFenetre: [
                v => (!v || v.length === 0 || (v >= 1 && v <= 100)) || 'Le nombre de fenêtres doit être entre 1 et 100'
            ],
            reglesPrix: [
                v => (!v || v.length === 0 || (v >= 50000 && v <= 1000000)) || 'Le prix doit être entre 50,000 et 1,000,000'
            ],
            reglesAnnee: [
                v => (!v || v.length === 0 || (v >= new Date(2004, 0, 1) && v <= new Date(2024, 0, 1))) || 'L\'année doit être entre 2004 et 2024'
            ],
            reglesNote: [
                v => (!v || v.length === 0 || (v >= 1 && v <= 5)) || 'La note doit être entre 1 et 5'
            ],
            categoriesPrix: ['bas', 'normal', 'élevé', 'arnaque'],
            villesDisponibles: ['Paris', 'Lyon', 'Marseille']
        };
    },
    mounted() {
        // Récupérer les données via l'API
        fetch('http://localhost:3000/logements')
            .then(response => response.json())
            .then(data => {
                this.logements = data;
                console.log(this.logements);
            })
            .catch(error => {
                console.error('Erreur lors de la récupération des données :', error);
            });
    },
    methods: {
        ajouterLogement() {
            const estNouveau = this.indexEdition === -1;
            const logementAAjouter = { ...this.nouveauLogement, id: estNouveau ? this.logements.length + 1 : this.logements[this.indexEdition].id };
            if (estNouveau) {
                this.logements.push(logementAAjouter);
            } else {
                Object.assign(this.logements[this.indexEdition], this.nouveauLogement);
            }
            this.sauvegarderDonnees(estNouveau);
        },

        sauvegarderDonnees(estNouveau) {
            fetch('http://localhost:3000/sauvegarder', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ logements: this.logements }),
            })
                .then((response) => response.json())
                .then((data) => {
                    alert('Données sauvegardées avec succès: ' + data.filePath);
                    this.reinitialiserFormulaire();  // Réinitialiser le formulaire après succès
                    if (!estNouveau) {
                        this.indexEdition = -1;  // Réinitialiser l'index d'édition
                    }
                })
                .catch((error) => {
                    console.error('Erreur lors de la sauvegarde des données:', error);
                });
        },

        reinitialiserFormulaire() {
            this.nouveauLogement = { nbChambres: '', superficie: '', nbFenetre: '', prix: '', annee: null, balcon: false, garage: false, note: 0, categoriePrix: '', ville: '' };
        },
        modifierLogement(logement) {
            this.nouveauLogement = { ...logement };
            this.indexEdition = this.logements.findIndex((l) => l.id === logement.id);
        },
        supprimerLogement(id) {
            this.logements = this.logements.filter((logement) => logement.id !== id);
        },
    },
};
</script>

<style scoped>
.logements-list {
    padding: 15px;
    background-color: #f5f5f5;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h2 {
    margin-bottom: 20px;
}
</style>
