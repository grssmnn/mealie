<template>
  <v-card :loading="isLoading">
    <v-img v-if="image" height="400" :src="image">
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
    </v-img>
    <br v-else />

    <ButtonRow
      @json="jsonEditor = true"
      @editor="jsonEditor = false"
      @save="createRecipe"
    />

    <div v-if="jsonEditor">
      <!-- Probably not the best way, but it works! -->
      <br />
      <br />
      <VJsoneditor
        v-model="recipeDetails"
        height="1500px"
        :options="jsonEditorOptions"
      />
    </div>

    <EditRecipe v-else v-model="recipeDetails" @upload="getImage" />
  </v-card>
</template>

<script>
import api from "../api";

import EditRecipe from "./RecipeEditor/EditRecipe";
import VJsoneditor from "v-jsoneditor";
import ButtonRow from "./UI/ButtonRow";
export default {
  components: {
    VJsoneditor,
    EditRecipe,
    ButtonRow,
  },
  data() {
    return {
      isLoading: false,
      fileObject: null,
      selectedFile: null,
      image: null,
      jsonEditor: false,
      jsonEditorOptions: {
        mode: "code",
        search: false,
        mainMenuBar: false,
      },
      recipeDetails: {
        name: "",
        description: "",
        image: "",
        recipeYield: "",
        recipeIngredient: [],
        recipeInstructions: [],
        slug: "",
        filePath: "",
        tags: [],
        categories: [],
        // dateAdded: "",
        notes: [],
        extras: [],
      },
    };
  },

  methods: {
    getImage(fileObject) {
      this.fileObject = fileObject;
      this.onFileChange();
    },
    onFileChange() {
      this.image = URL.createObjectURL(this.fileObject);
    },

    async createRecipe() {
      this.isLoading = true;

      if (this.fileObject) {
        this.recipeDetails.image = this.fileObject.name;
      } 
      let slug = await api.recipes.create(this.recipeDetails);

      if (this.fileObject) {
        await api.recipes.updateImage(slug, this.fileObject);
      }

      this.isLoading = false;

      this.$router.push(`/recipe/${slug}`);
    },
  },
};
</script>

<style>
.img-input {
  position: absolute;
  bottom: 0;
}
</style>