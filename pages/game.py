import streamlit as st
from copy import deepcopy
import random


st.set_page_config(
    page_title='Multiple pages',
    layout="wide"
)
if 'round' not in st.session_state:
    st.session_state.round = 1
    



income_constant_mapping = {
    '爱迪生': 2,
    '特斯拉': 1,
    '慈禧': 0.7,
    '尼古拉斯二世': 1,
    '袁隆平': 3,
    '成吉思汗': 1,
    '秦始皇': 1,
    '明治天皇': 1,
    '罗斯福': 0.5,
    '刘秀': 1,
    '奥本海默': 1,
    '腓特烈二世': 1
}

build_constant_mapping = {
    '爱迪生': 1,
    '特斯拉': 1,
    '慈禧': 0.9,
    '尼古拉斯二世': 1,
    '袁隆平': 1,
    '成吉思汗': 1,
    '秦始皇': 0.5,
    '明治天皇': 1,
    '罗斯福': 1,
    '刘秀': 1,
    '奥本海默': 1,
    '腓特烈二世': 1
}

soldier_constant_mapping = {
    '爱迪生': 1,
    '特斯拉': 1,
    '慈禧': 1,
    '尼古拉斯二世': 1,
    '袁隆平': 1,
    '成吉思汗': 1,
    '秦始皇': 0.5,
    '明治天皇': 1,
    '罗斯福': 1,
    '刘秀': 1,
    '奥本海默': 1,
    '腓特烈二世': 1
}



deduction_mapping = {
    '爱迪生': 225,
    '特斯拉': 0,
    '慈禧': 0,
    '尼古拉斯二世': 150,
    '袁隆平': 250,
    '成吉思汗': 150,
    '秦始皇': 250,
    '明治天皇': 225,
    '罗斯福': 175,
    '刘秀': 300,
    '奥本海默': 170,
    '腓特烈二世': 400
}

if 'inflation_rate' not in st.session_state:
    st.session_state.inflation_rate = 0
st.title(f'Round {st.session_state.round}')



col1, col2, col3, col4, col5 = st.columns(5)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False


num_players = 4
def initialize_player_files(num_players):
    player_resource = dict()
    add_resource = dict()
    for i in range(1, num_players+1):
        res = {'money':1000}
        player_resource[i] = res
        add_resource[i] = dict()
    
    return player_resource, add_resource

if 'player_resource_dict' not in st.session_state:
    player_resource_dict, player_addresource_dict = initialize_player_files(num_players)
    st.session_state.player_resource_dict = player_resource_dict
    st.session_state.player_addresource_dict = player_addresource_dict

if 'piece_killed_dict' not in st.session_state:
    st.session_state.piece_killed_dict = dict()
    
if 'player_idx' not in st.session_state:
    st.session_state.player_idx = 1

if 'num_building' not in st.session_state:
    st.session_state.num_building = 0
    
if 'num_pieces' not in st.session_state:
    st.session_state.num_pieces = 0
    
if 'prev_I' not in st.session_state:
    st.session_state.prev_I = 1
    
if 'resource_automating_counter' not in st.session_state:
    st.session_state.resource_automating_counter = {1:dict(), 2:dict(), 3:dict(), 4:dict()}

if 'total_buildings_count' not in st.session_state:
    st.session_state.total_buildings_count = 0
    
if 'players_buildings_count' not in st.session_state:
    st.session_state.players_buildings_count = [None, 0, 0, 0, 0]

    
global_player_resource_dict = st.session_state.player_resource_dict
global_player_addresource_dict = st.session_state.player_addresource_dict
player_idx = st.session_state.player_idx

char_list = ('爱迪生', '特斯拉', '慈禧', '尼古拉斯二世', '袁隆平', '成吉思汗', '秦始皇', '明治天皇', '罗斯福', '刘秀', '奥本海默', '腓特烈二世')
option = char_list[st.session_state.char_idx_tuple[player_idx-1]]


if 'resource_to_cost_mapping' not in st.session_state:
    st.session_state.resource_to_cost_mapping = {'wood':25, 'iron ore':100, 'gold':250, 'crude oil':200, 'fish':20, 'crop':20, 'meat':25, 'stone':25, 'coal':50, 'animal':20, 'steel':200, 'fine iron':150, 'gasoline':300, 'food':110, 'building material':500}

if 'prev_p' not in st.session_state:
    st.session_state.prev_p = 0

if 'first_round' not in st.session_state:
    st.session_state.first_round = True

if 'collecting_plants_dict' not in st.session_state:
    st.session_state.collecting_plants_dict = {1:dict(), 2:dict(), 3:dict(), 4:dict()}
    
if 'processing_plants_dict' not in st.session_state:
    st.session_state.processing_plants_dict = {1:dict(), 2:dict(), 3:dict(), 4:dict()}
    
if 'broke_counter' not in st.session_state:
    st.session_state.broke_counter = [None, 0, 0, 0, 0]


processing_plant_product_price_constant = {'steel':3, 'fine iron':2, 'gasoline':2, 'food':2, 'building material':2}
ratio = {'wood':25, 'iron ore':50, 'gold':250, 'crude oil':200, 'fish':20, 'crop':20, 'meat':20, 'stone':25, 'coal':100, 'animal':25}
resource_to_amount = {'wood':3, 'iron ore':2, 'gold':1, 'crude oil':1, 'fish':3, 'crop':3, 'meat':2, 'stone':3, 'coal':3, 'animal':3}
class resource: 
    #Initialize give how many, give what and what is the cost of that resource
    def __init__(self, label, amount, build_cost, little=False):
        self.label = label
        self.amount = amount
        self.little = little
        self.build_cost = build_cost
        
    def display_price(self):
        st.text(f'Building Cost: {self.build_cost}')
        
    def display_title(self):
        st.subheader(f'{self.label.capitalize()} Resource')
    
    def display_build(self):
        if not self.little:
            st.button(f'Build {self.label} Collection', on_click=self.build)

    def build(self):
        player_res = st.session_state.player_resource_dict[player_idx]
        self.build_cost *= build_constant_mapping[option]
        cost = self.build_cost
        
        if option == '秦始皇':
            cost = round(cost/2)
            
        if player_res['money'] >= cost and st.session_state.total_buildings_count <= 28 and st.session_state.players_buildings_count[player_idx] <= 15:
            st.session_state.player_resource_dict[player_idx]['money'] -= cost
            st.session_state.players_buildings_count[player_idx] += 1
            st.session_state.total_buildings_count += 1
            
            if self.label not in st.session_state.collecting_plants_dict[player_idx]:
                st.session_state.collecting_plants_dict[player_idx][self.label] = 1 
                
            else:
                st.session_state.collecting_plants_dict[player_idx][self.label] += 1
                

    def display_button(self):
        if not self.little:
            st.button(f'Get {self.label}', on_click=self.add_player_resource)
        else:
            st.button(f'Get {self.label}*1', on_click=self.add_player_resource)
    
    def destroy_building(self):
        if st.session_state.collecting_plants_dict[player_idx][self.label] > 0: #if have
            st.session_state.collecting_plants_dict[player_idx][self.label] -= 1
            
        
    def display_generate_resource(self):
        st.write(f'Generates: {self.label}*{self.amount}')
    
    def add_player_resource(self):
        global global_player_resource_dict
        player_resource = global_player_resource_dict[player_idx]
        
        if self.label in player_resource:
            player_resource[self.label] += self.amount
            
        else:
            player_resource[self.label] = self.amount
        
        global_player_resource_dict[player_idx] = player_resource
        st.session_state.player_resource_dict = global_player_resource_dict

class processing_plant:
    #Initialize name and resource needed to build this processing plant
    def __init__(self, required_resource_map:dict, accept_resource_list, product, title=None):
        self.required_resource_map = required_resource_map
        self.accept_resource_list = accept_resource_list
        self.product = product
        self.stored_res_and_amount = dict()
        self.title = title if title is not None else product

        
    def display_price(self):
        st.text(f'Building Cost: {list(self.required_resource_map.values())[0]}')
        
    def display_title(self):
        st.subheader(f'{self.title.capitalize()} Processing Plant')
    

    def display_build_button(self):
        st.button(f'Build {self.product.capitalize()} Processing Plant', on_click=self.build)

    def display_invest_button(self):
        st.button(f'Invest resource to {self.title.capitalize()} Processing Plant', on_click=self.invest)

            
    def build(self):
        global global_player_resource_dict
        player_resource = deepcopy(global_player_resource_dict[player_idx])
        ok = True

        for res_name, amount in self.required_resource_map.items():
            amount = round(amount * build_constant_mapping[option], 1)
            if option == '秦始皇':
                amount = round(amount/2)
            if res_name in player_resource:
                if player_resource[res_name] >= amount:
                    player_resource[res_name] -= amount
                    
                else: #Do not have enough
                    print('Do not have enough')
                    ok = False
            
            else: #Do not have the resource
                print('Do not have enough')
                ok = False
        if ok and st.session_state.players_buildings_count[player_idx] <= 15 and st.session_state.total_buildings_count <= 28:
            st.session_state.players_buildings_count[player_idx] += 1
            st.session_state.total_buildings_count += 1
            
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
            
            if self.product not in st.session_state.processing_plants_dict[player_idx]:
                st.session_state.processing_plants_dict[player_idx][self.product] = 1
                
            else:
                st.session_state.processing_plants_dict[player_idx][self.product] += 1
            

           
    def invest(self): #Invest what resource, and how much
        global global_player_resource_dict
        global global_player_addresource_dict
        player_resource = global_player_resource_dict[player_idx]
        next_round_add_resource = global_player_addresource_dict[player_idx]
        ok = True
        
        for key, value in self.stored_res_and_amount.items():
            if value == 0: continue
            elif key not in player_resource or player_resource[key] < value:
                ok = False
                break
        
                
        if ok:
            invested_amount = 0
            for key, value in self.stored_res_and_amount.items():
                if value == 0: continue
                invested_amount += st.session_state.resource_to_cost_mapping[key]*value
                player_resource[key] -= value
            
            invested_amount *= processing_plant_product_price_constant[self.product]
            num_product = invested_amount/st.session_state.resource_to_cost_mapping[self.product]
            
            if self.product in next_round_add_resource:
                next_round_add_resource[self.product] += round(num_product)
            else:
                next_round_add_resource[self.product] = round(num_product)

            
            global_player_addresource_dict[player_idx] = next_round_add_resource
            st.session_state.player_addresource_dict = global_player_addresource_dict
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
            st.session_state.num_building += 1
            self.stored_res_and_amount = dict()
        else:
            print('Not enough resource')
        
class piece:
    def __init__(self, cost, name):
        self.cost = cost
        if option == '秦始皇':
            self.cost = round(cost/2)
        self.name = name
        
    def display_buy_button(self):
        st.button(f'Buy {self.name} piece', on_click=self.buy)
        
    def buy(self):
        global global_player_resource_dict
        player_resource = deepcopy(global_player_resource_dict[player_idx])
        ok = True
        
        if player_resource['money'] >= self.cost:
            player_resource['money'] -= self.cost
            
        else:
            ok = False
            
        if ok:
            global_player_resource_dict[player_idx] = player_resource
            st.session_state.player_resource_dict = global_player_resource_dict
            st.session_state.num_pieces += 1


def generate_player_info(player_idx):
    player_resource = global_player_resource_dict[player_idx]
    result = f'{st.session_state.player_name_list[player_idx]}: <br/>'
    result += f'Character: {option}<br/>'
    result += f'Resource: | '
    
    for key, value in player_resource.items():
        value = round(value, 0)
        result += f'{key}:{value}'
        result += ' | '
    
    
    result += '<br/>'
    result += 'Collecting Plants: | '
    collecting_plants_dict = st.session_state.collecting_plants_dict[player_idx]

    for plant, amount in collecting_plants_dict.items():
        result += f'{plant}:{amount} | '
        
    result += '<br/>'
    
    result += 'Processing Plants: | '
    for plant, amount in st.session_state.processing_plants_dict[player_idx].items():
        result += f'{plant}:{amount} | '
    
    
    
    return result

bottom_right_style = """
    position: fixed;
    bottom: 0;
    right: 0;
    padding: 10px;
    color:green;
    font-size:20px;
    bold:true;
"""

def buy_insurance():
    cost = 500
    global global_player_resource_dict
    player_resource = deepcopy(global_player_resource_dict[player_idx])
    ok = True
    
    if player_resource['money'] >= cost:
        player_resource['money'] -= cost
        
    else:
        ok = False
        
    if ok:
        global_player_resource_dict[player_idx] = player_resource
        st.session_state.player_resource_dict = global_player_resource_dict
    

basic_info = generate_player_info(player_idx)
st.markdown("<div style='" + bottom_right_style + f"'>{basic_info}</div>", unsafe_allow_html=True)

def sell(res_name, amount):
    global global_player_resource_dict
    player_resource = global_player_resource_dict[player_idx]
        
    if res_name in player_resource and player_resource[res_name] >= amount:
        player_resource[res_name] -= amount
        money_profit = st.session_state.resource_to_cost_mapping[res_name]
        
        player_resource['money'] += money_profit * income_constant_mapping[option] * amount
        
    global_player_resource_dict[player_idx] = player_resource
    st.session_state.player_resource_dict = global_player_resource_dict

def next_player():
    global player_idx
    global global_player_resource_dict
    
    
    player_resource = global_player_resource_dict[player_idx]
    next_round_add_resource = global_player_addresource_dict[player_idx]
    
    
    if st.session_state.player_resource_dict[player_idx]['money'] < deduction_mapping[option]:
        st.session_state.player_resource_dict[player_idx]['money'] = 0
        
    else:
        st.session_state.player_resource_dict[player_idx]['money'] -= deduction_mapping[option]
    
    constant = 1.75 if option == '爱迪生' else 1
    for key, value in next_round_add_resource.items():
        if key in player_resource:
            player_resource[key] += round(value*constant)
        else:
            player_resource[key] = round(value*constant)
    
    global_player_resource_dict[player_idx] = player_resource
    st.session_state.player_resource_dict = global_player_resource_dict
    
    while True:
        player_idx += 1
        #Update player idx
        if player_idx > 4:
            player_idx = 1
            
        if not st.session_state.player_dead_list[player_idx]: #If next player alive:
            break
        
    if player_idx == 1:
        st.session_state.round += 1

    st.session_state.player_idx = player_idx
    st.session_state.player_addresource_dict[player_idx] = dict()
    
    next_player_add_resource = st.session_state.collecting_plants_dict[player_idx]


    for resource, amount in next_player_add_resource.items():
        constant2 = resource_to_amount[resource]
        if resource not in st.session_state.player_resource_dict[player_idx]:
            st.session_state.player_resource_dict[player_idx][resource] = amount * constant2
            
        else:
            st.session_state.player_resource_dict[player_idx][resource] += amount * constant2
            
    st.session_state.first_round = True
    
print(st.session_state.resource_to_cost_mapping)   
 
def calculate_and_adjust_value_by_inflation_rate():
    try:
        cash = 0
        resource_total_cost = 0
        prev_I = st.session_state.prev_I
        
        for _, player_resource_dict in st.session_state.player_resource_dict.items():
            for key, value in player_resource_dict.items():
                if key == 'money':
                    cash += value
                else:
                    if key in ratio:
                        resource_total_cost += value*ratio[key]
        
        resource_total_cost *= prev_I 
        num_building = st.session_state.num_building
        num_pieces = st.session_state.num_pieces
        total_money_value = resource_total_cost + cash + 50*num_building + 100*num_pieces
        cur_p = total_money_value/4
        
        prev_p = cur_p*0.95 if st.session_state.prev_p == 0 else st.session_state.prev_p

        constant = random.choice([0.1, -0.1])

        cur_I = 1+(((((cur_p-prev_p)/cur_p)) * constant)*2)

        res_to_cost_mapping = st.session_state.resource_to_cost_mapping
        st.session_state.inflation_rate = cur_I
        
        for key, value in res_to_cost_mapping.items():
            res_to_cost_mapping[key] = round(value * (cur_I), 0)
            
        st.session_state.prev_I = cur_I
        st.session_state.resource_to_cost_mapping = res_to_cost_mapping
        st.session_state.prev_p = cur_p

    except:
        pass
    
def count_killed_pieces():
    if option == '成吉思汗':
        st.session_state.player_resource_dict[player_idx]['money'] += 175
        
    if option == '奥本海默':
        st.session_state.player_resource_dict[player_idx]['money'] += 50
        
if player_idx == 1 and st.session_state.first_round and st.session_state.player_resource_dict[player_idx]['money'] != 1000:
    print(st.session_state.player_resource_dict[player_idx])
    calculate_and_adjust_value_by_inflation_rate()

st.header(f'Inflation rate: {round(st.session_state.inflation_rate, 3)}')

if 'player_dead_list' not in st.session_state:
    st.session_state.player_dead_list = [False, False, False, False, False]

player_dead = st.session_state.player_dead_list

if st.session_state.player_resource_dict[player_idx]['money'] == 0 and st.session_state.first_round:
    st.session_state.broke_counter[player_idx] += 1
    
    
if st.session_state.player_resource_dict[player_idx]['money'] > 0:
    st.session_state.broke_counter[player_idx] = 0
    
with col1:
    wood_res1 = resource('wood', 1, 0, True)
    
    iron_res1 = resource('iron ore', 1, 0, True)
    
    gold_res1 = resource('gold', 1, 0, True)
    
    crude_res1 = resource('crude oil', 1, 0, True)
    
    fish_res1 = resource('fish', 1, 0, True)

    crop_res1 = resource('crop', 1, 0, True)
    
    meat_res1 = resource('meat', 1, 0, True)
    
    stone_res1 = resource('stone', 1, 0, True)

    coal_res1 = resource('coal', 1, 0, True)

    animal_res1 = resource('animal', 1, 0, True)

    wood_res = resource('wood', 3, 500)
    wood_res.display_title()
    wood_res.display_price()
    wood_res.display_build()
    wood_res.display_generate_resource()
    wood_res1.display_button()
    st.text("")
    st.text("")
    
    iron_res = resource('iron ore', 2, 1000)
    iron_res.display_title()
    iron_res.display_price()
    iron_res.display_build()
    iron_res.display_generate_resource()
    iron_res1.display_button()
    st.text("")
    st.text("")
    
    gold_res = resource('gold', 1, 2500)
    gold_res.display_title()
    gold_res.display_price()
    gold_res.display_build()
    gold_res.display_generate_resource()
    gold_res1.display_button()
    st.text("")
    st.text("")
    
    crude_res = resource('crude oil', 1, 2000)
    crude_res.display_title()
    crude_res.display_price()
    crude_res.display_build()
    crude_res.display_generate_resource()
    crude_res1.display_button()
    st.text("")
    st.text("")
    
    fish_res = resource('fish', 3, 400)
    fish_res.display_title()
    fish_res.display_price()
    fish_res.display_build()
    fish_res.display_generate_resource()
    fish_res1.display_button()
    st.text("")
    st.text("")
    
    crop_res = resource('crop', 3, 350)
    crop_res.display_title()
    crop_res.display_price()
    crop_res.display_build()
    crop_res.display_generate_resource()
    crop_res1.display_button()
    st.text("")
    st.text("")
    
    meat_res = resource('meat', 2, 350)
    meat_res.display_title()
    meat_res.display_price()
    meat_res.display_build()
    meat_res.display_generate_resource()
    meat_res1.display_button()
    st.text("")
    st.text("")
    
    stone_res = resource('stone', 3, 300)
    stone_res.display_title()
    stone_res.display_price()
    stone_res.display_build()
    stone_res.display_generate_resource()
    stone_res1.display_button()
    st.text("")
    st.text("")

    coal_res = resource('coal', 3, 750)
    coal_res.display_title()
    coal_res.display_price()
    coal_res.display_build()
    coal_res.display_generate_resource()
    coal_res1.display_button()
    st.text("")
    st.text("")
    
    animal_res = resource('animal', 3, 300)
    animal_res.display_title()
    animal_res.display_price()
    animal_res.display_build()
    animal_res.display_generate_resource()
    animal_res1.display_button()
    st.text("")
    st.text("")
    
with col2:
    #Steel plant
    steel_dict = dict()
    steel_plant = processing_plant({'money':1200}, ['fine iron', 'coal'], 'steel')
    steel_plant.display_title()
    steel_plant.display_price()
    steel_plant.display_build_button()
    fine_iron_for_steel_plant = st.number_input("Number of fine iron to invest to steel plant:", value=0, placeholder="Type a number...")
    coal_for_steel_plant = st.number_input("Number of coal to invest to steel plant", value=0, placeholder="Type a number...")
    steel_dict['fine iron'] = fine_iron_for_steel_plant
    steel_dict['coal'] = coal_for_steel_plant
    steel_plant.stored_res_and_amount = steel_dict
    steel_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Steel plant
    fine_iron_dict = dict()
    fine_iron_plant = processing_plant({'money':800}, ['iron ore'], 'fine iron')
    fine_iron_plant.display_title()
    fine_iron_plant.display_price()
    fine_iron_plant.display_build_button()
    iron_ore_for_fine_iron_plant = st.number_input("Number of iron ore to invest to fine iron plant:", value=0, placeholder="Type a number...")
    fine_iron_dict['iron ore'] = iron_ore_for_fine_iron_plant
    fine_iron_plant.stored_res_and_amount = fine_iron_dict
    fine_iron_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Refinery plant
    refinery_dict = dict()
    refinery_plant = processing_plant({'money':1600}, ['crude oil'], 'gasoline', 'refinery')
    refinery_plant.display_title()
    refinery_plant.display_price()
    refinery_plant.display_build_button()
    crude_oil_for_refinery_plant = st.number_input("Number of crude oil to invest to refinery plant:", value=0, placeholder="Type a number...")
    refinery_dict['crude oil'] = crude_oil_for_refinery_plant
    refinery_plant.stored_res_and_amount = refinery_dict
    refinery_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Food plant
    food_dict = dict()
    food_plant = processing_plant({'money':1000}, ['fish', 'crop', 'meat'], 'food')
    food_plant.display_title()
    food_plant.display_price()
    food_plant.display_build_button()
    fish_for_food_plant = st.number_input("Number of fish to invest to food plant:", value=0, placeholder="Type a number...")
    crop_for_food_plant = st.number_input("Number of crop to invest to food plant:", value=0, placeholder="Type a number...")
    meat_for_food_plant = st.number_input("Number of meat to invest to food plant:", value=0, placeholder="Type a number...")
    food_dict['fish'] = fish_for_food_plant
    food_dict['crop'] = crop_for_food_plant
    food_dict['meat'] = meat_for_food_plant
    food_plant.stored_res_and_amount = food_dict
    food_plant.display_invest_button()
    st.write('')
    st.write('')
    
    #Building material
    building_material_dict = dict()
    building_material_plant = processing_plant({'money':800}, ['wood', 'stone', 'fine iron'], 'building material')
    building_material_plant.display_title()
    building_material_plant.display_price()
    building_material_plant.display_build_button()
    wood_for_building_material_plant = st.number_input("Number of wood to invest to building plant:", value=0, placeholder="Type a number...")
    stone_for_building_material_plant = st.number_input("Number of stone to invest to building plant:", value=0, placeholder="Type a number...")
    fine_iron_for_building_material_plant = st.number_input("Number of fine iron to invest to building plant:", value=0, placeholder="Type a number...")
    building_material_dict['wood'] = wood_for_building_material_plant
    building_material_dict['stone'] = stone_for_building_material_plant
    building_material_dict['fine iron'] = fine_iron_for_building_material_plant
    building_material_plant.stored_res_and_amount = building_material_dict
    building_material_plant.display_invest_button()
    st.write('')
    st.write('')

with col3:
    for res in st.session_state.resource_to_cost_mapping:
        
        amount = st.number_input(f'Number of {res}', value=0, placeholder="Type a number...")
        st.button(f'Sell {res}', on_click=sell, args=(res, amount))

with col4:
    castle_piece = piece(330, 'castle')
    castle_piece.display_buy_button()
    
    bishop_piece = piece(200, 'bishop')
    bishop_piece.display_buy_button()
    
    knight_piece = piece(200, 'knight')
    knight_piece.display_buy_button()
    
    soldier_piece = piece(65, 'soldier')
    soldier_piece.display_buy_button()
    
    st.button('Buy insurance', on_click=buy_insurance)
    
   
with col5:
    st.button('Killed a piece', on_click=count_killed_pieces)
    st.button('Next player', on_click=next_player)
    
    for player_number in range(1, 5):
        constant = st.session_state.broke_counter[player_number] == 3 or st.session_state.player_dead_list[player_number]
        st.session_state.player_dead_list[player_number] = st.checkbox(f"{st.session_state.player_name_list[player_number]} Game Over", constant)

if st.session_state.first_round:
    st.session_state.first_round = False