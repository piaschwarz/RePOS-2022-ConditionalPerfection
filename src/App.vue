<template>
  <Experiment title="Experiment">
    <InstructionScreen :title="'Willkommen'">
      Vielen Dank für Ihr Interesse an unserer Studie. 
      Untersuchungen wie diese tragen dazu bei zu verstehen, wie der Mensch Sprache verarbeitet.
      Damit können zum Beispiel Interaktionen zwischen Mensch und Maschine, die immer mehr Einzug in unseren 
      Alltag finden, besser gestaltet werden.
      <br />
      <br />
      Um das Experiment durchzuführen, müssen Sie die Studie an einem Laptop oder Computer durchführen.
      Die Bearbeitungszeit dauert im Durchschnitt ca. 15 Minuten. Alle Fragen können jedoch im eigenen 
      Tempo bearbeitet werden.
      <br />
      <br />
      Bevor die Studie beginnt, bekommen Sie auf der nächsten Seite noch genauere Anweisungen.
    </InstructionScreen>

    <InstructionScreen :title="'Ablauf des Experiments'">
      Im Folgenden wird Ihnen zunächst jeweils ein Text gezeigt, der eine Alltagssituation beschreibt. 
      Lesen Sie diesen bitte aufmerksam durch.<br>
      Sobald Sie den Text gelesen und verstanden haben, klicken Sie auf Weiter, dann erscheinen 
      nacheinander Fragen und Antworten zum Text.<br>
      Am Ende jedes Textes bekommen Sie eine Frage gestellt, die Sie mit Ja oder Nein beantworten können. 
      <br />
      <br />
      Im Nachgang stellen wir Ihnen noche ein paar Fragen zu Ihrer Person und Sie haben die Möglichkeit, 
      uns Feedback zu geben. Hierbei sind alle Angaben anonym und es wird zu keinem Zeitpunkt nach 
      Ihrem Namen oder Kontaktadresse gefragt.
      <br />
      <br />
      Mit Klick auf Next starten Sie die Studie.
    </InstructionScreen>


    <template v-for="(tvj_task, i) of test_filler_items">
      <Screen>
        <button @click="getStartTime(); $magpie.nextScreen()">Zum Text</button>
      </Screen>
      <Screen>
        <br />
        {{tvj_task.context}}
        <button @click="$magpie.nextScreen()">Weiter</button>
      </Screen>
      <Screen>
        <br />
        {{tvj_task.context}}
        <br />
        <br />
        {{tvj_task.question}}
        <button @click="$magpie.nextScreen()">Weiter</button>
      </Screen>
      <Screen>
        <br />
        {{tvj_task.context}}
        <br />
        <br />
        {{tvj_task.question}}
        <br />
        <br />        
        {{tvj_task.answer}}
        <button @click="$magpie.nextScreen()">Weiter zur Frage</button>
      </Screen>

      <ForcedChoiceScreen
        :key="i"
        :options="['Ja', 'Nein']"
      >
        <template #stimulus>
            <p>{{tvj_task.context}}</p>
            <br />   
            <p>{{tvj_task.question}}</p>
            <p>{{tvj_task.answer}}</p>  
            <br /> 
            <br />
            <br /> 
            <p><b>{{tvj_task.tvjudgement}}</b></p>
          <Record :data="{
              'group': tvj_task.group,
              'item_type': tvj_task.item.split('_')[0],
              'item_answer_type': tvj_task.item.split('_')[2],
              'item_number': tvj_task.item.split('_')[1],
              'trial_number': i+1,
              'stopwatch_ms': getResponseTime()
            }" />
        </template>
        
      </ForcedChoiceScreen>
    </template>


    <Screen :title="'Zusätzliche Information'">
      <p>Nun stellen wir Ihnen noch Fragen zu Ihrer Person.<br>
        Alle Angaben sind optional, helfen uns aber beim Auswerten der Ergebnisse.
      </p>
      <br>
      <div>
        <legend><b>Ist deutsch Ihre Muttersprache?</b></legend>
        <input type="radio" id="ja" value="Ja" v-model="$magpie.measurements.german_native" />
        <label for="ja">Ja</label><br>
        <input type="radio" id="nein" value="Nein" v-model="$magpie.measurements.german_native" />
        <label for="nein">Nein</label><br>
        <input type="radio" id="keineAngabe" value="KeineAngabe" v-model="$magpie.measurements.german_native" checked>
        <label for="keineAngabe">Keine Angabe</label>
      </div>
      <br>
      <div>
          <p>Haben Sie umfangreiche Kenntnisse oder großes Wissen über Linguistik?<br>
            Bitte beantworten Sie die Frage bezogen auf folgende Teilbereiche der Linguistik:</p>
          <legend><b>Pragmatik</b></legend>
          <input type="radio" id="ja" value="Ja" v-model="$magpie.measurements.knowledge_pragmatics" />
          <label for="ja">Ja</label><br>
          <input type="radio" id="nein" value="Nein" v-model="$magpie.measurements.knowledge_pragmatics" />
          <label for="nein">Nein</label>
          <br>
          <br>
          <legend><b>Logik</b></legend>
          <input type="radio" id="ja" value="Ja" v-model="$magpie.measurements.knowledge_logic" />
          <label for="ja">Ja</label><br>
          <input type="radio" id="nein" value="Nein" v-model="$magpie.measurements.knowledge_logic" />
          <label for="nein">Nein</label>
      </div>
      <br>
      <div>
        <p>Hier ist Platz, falls Sie Anmerkungen haben:</p>
        <TextareaInput :response.sync= "$magpie.measurements.comment" />
      </div>
      <br />
      <button @click="$magpie.addExpData({
          german_native: $magpie.measurements.german_native,
          knows_pragmatics: $magpie.measurements.knowledge_pragmatics,
          knows_logic: $magpie.measurements.knowledge_logic,
          comments: $magpie.measurements.comment
        }); $magpie.nextScreen()">Befragung abschließen</button>
    </Screen>

    <!-- While developing your experiment, using the DebugResults screen is fine,
      once you're going live, you can use the <SubmitResults> screen to automatically send your experimental data to the server. -->
    <!--<DebugResultsScreen /> -->
    <SubmitResultsScreen />
  </Experiment>
</template>

<script>
// Load data from csv files as javascript arrays with objects
//import test_filler_items_A from '../trials/test_filler_items_A_OLD.csv'; //for test purposes
//import test_filler_items_B from '../trials/test_filler_items_B_OLD.csv'; //for test purposes
import test_filler_items_A from '../trials/test_filler_items_A.csv';
import test_filler_items_B from '../trials/test_filler_items_B.csv';
import _ from 'lodash';

var startTime;
var endTime;

export default {
  name: 'App',
  data() {
    return {
      test_filler_items: _.shuffle(_.sample([test_filler_items_A, test_filler_items_B])),
      startTime,
      endTime,
      // Expose lodash.range to template above
      range: _.range
    };
  },
  methods: {
    getStartTime() {
      startTime = Date.now();
      //console.log("STARTED STOPWATCH: ", startTime.toString())
    },
    getResponseTime() {
      endTime = Date.now();
      //console.log("STOPPED STOPWATCH: ", endTime.toString())
      var miliseconds = endTime - startTime;
      //console.log("STOPWATCH time in milisecs: ", miliseconds)
      return miliseconds
    }
  },
};

</script>
